/**
 * Dispatcher.java
 * Sep 3, 2010
 */
package uk.ac.kcl.cch.eats.dispatcher;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.JAXBException;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.NameValuePair;
import org.apache.http.ParseException;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.CookieStore;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.params.HttpClientParams;
import org.apache.http.client.protocol.ClientContext;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.impl.client.BasicCookieStore;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpParams;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HttpContext;
import org.apache.http.util.EntityUtils;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;

import uk.ac.kcl.cch.eats.eatsml.Collection;
import uk.ac.kcl.cch.eats.eatsml.Entity;

/**
 * This class connects to the EATS server and handles requests between the
 * client and the server.
 * 
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 */
public class Dispatcher {

	// Constants

	public static final String DEFAULT_ENCODING = "UTF-8";

	/**
	 * URL for retrieving the base EATSML information.
	 */
	public static final String BASE_DOCUMENT_URL = "export/eatsml/base/";

	/**
	 * Base URL prefix for editing entities. It needs to be concatenated
	 * with the entity id and the Base URL suffix.
	 */
	public static final String EDIT_ENTITY_PREFIX_URL = "entity/";
	
	/**
	 * Base URL suffix for editing entities. It needs to be added to the
	 * end of the Base URL prefix and the entity id.
	 */
	public static final String EDIT_ENTITY_SUFFIX_URL = "/edit/";

	/**
	 * URL for importing EATSML.
	 */
	public static final String IMPORT_URL = "import/";

	/**
	 * URL for processed imports.
	 */
	public static final String PROCESSED_IMPORT_URL = "annotated/";

	/**
	 * URL for searching and retrieving results. Search terms are concatenated
	 * with this URL.
	 */
	public static final String LOOKUP_NAME_URL = "search/eatsml/";

	/**
	 * URL that retrieves information about the XSLTs to transform EATSML.
	 */
	public static final String XSLT_URL = "edit/export/xslt/";

	// Properties

	/**
	 * URL of the EATS server.
	 */
	private String serverUrl = null;

	/**
	 * EATS server user.
	 */
	private String username = null;

	/**
	 * EATS server password.
	 */
	private String password = null;

	/**
	 * EATS server proxy username.
	 */
	private String proxyUsername = null;

	/**
	 * EATS server proxy password.
	 */
	private String proxyPassword = null;

	/**
	 * String that stores infrastructural information from the EATS server.
	 */
	private String baseDoc = null;

	/**
	 * HTTP client.
	 */
	private DefaultHttpClient httpClient = null;

	/**
	 * HTTP parameters.
	 */
	private HttpParams httpParams = null;

	/**
	 * Cookie store for the HTTP requests.
	 */
	private CookieStore cookieStore = null;

	/**
	 * Local HTTP context.
	 */
	private HttpContext localContext = null;

	/**
	 * Django/EATS server csrf token.
	 */
	private String csrfToken = null;

	// Constructor(s)

	/**
	 * Creates a new Dispatcher.
	 * 
	 * @param serverUrl
	 *            the EATS server URL
	 * @param username
	 *            the EATS server username
	 * @param password
	 *            the EATS server password
	 * @param proxyUsername
	 *            the EATS server proxy username
	 * @param proxyPassword
	 *            the EATS server proxy password
	 */
	public Dispatcher(String serverUrl, String username, String password,
			String proxyUsername, String proxyPassword) {
		this.serverUrl = serverUrl;
		this.username = username;
		this.password = password;
		this.proxyUsername = proxyUsername;
		this.proxyPassword = proxyPassword;

		// creates new HTTP client
		httpClient = new DefaultHttpClient();
		// creates new HTTP parameters
		httpParams = new BasicHttpParams();
		// do not follow redirects
		HttpClientParams.setRedirecting(httpParams, false);

		if (this.proxyUsername != null && this.proxyUsername != null) {
			httpClient.getCredentialsProvider().setCredentials(
					AuthScope.ANY,
					new UsernamePasswordCredentials(this.proxyUsername,
							this.proxyPassword));
		}

		// creates a local instance of cookie store
		cookieStore = new BasicCookieStore();
		// creates local HTTP context
		localContext = new BasicHttpContext();
		// binds custom cookie store to the local context
		localContext.setAttribute(ClientContext.COOKIE_STORE, cookieStore);

		// sets the transformer to saxon
		System.setProperty("javax.xml.transform.TransformerFactory",
				"net.sf.saxon.TransformerFactoryImpl");
	}

	// Methods

	/**
	 * Logs in to the EATS server.
	 * 
	 * @throws DispatcherException
	 *             in case of any failure.
	 */
	public void login() throws DispatcherException {

		HttpResponse response = null;

		try {
			// creates a new get request to get the base document
			HttpGet get = new HttpGet(serverUrl + BASE_DOCUMENT_URL);
			get.setParams(httpParams);

			// executes the request and gets the response
			response = httpClient.execute(get, localContext);

			// checks the response is valid
			checkResponse(response);

			// gets the response status
			int status = response.getStatusLine().getStatusCode();

			// releases resources for the following connections
			consumeResponseEntity(response);

			// if the server redirects login is required
			if (status == HttpStatus.SC_MOVED_TEMPORARILY) {
				// gets the login url
				String loginUrl = response.getHeaders("Location")[0].getValue();

				// creates a new get request to get the login form
				get = new HttpGet(loginUrl);
				get.setParams(httpParams);

				// executes the get request
				response = httpClient.execute(get, localContext);

				if (response != null && response.getEntity() != null) {
					// gets the crsf token
					csrfToken = getCsrf(response.getEntity());
				} else {
					throw new DispatcherException(
							"unable to get the login form");
				}

				// creates a list to store the post request parameters
				List<NameValuePair> params = new ArrayList<NameValuePair>();
				params.add(new BasicNameValuePair("username", username));
				params.add(new BasicNameValuePair("password", password));
				params.add(new BasicNameValuePair("csrfmiddlewaretoken",
						csrfToken));

				// creates a new form entity
				UrlEncodedFormEntity entity = new UrlEncodedFormEntity(params,
						DEFAULT_ENCODING);

				// creates a new post request
				HttpPost post = new HttpPost(loginUrl);

				// adds the form entity to the post request
				post.setEntity(entity);

				// executes the post request to login
				response = httpClient.execute(post, localContext);

				// checks the response is valid
				checkResponse(response);

				// gets the response status
				status = response.getStatusLine().getStatusCode();

				// login is successful if the server redirects
				if (status != HttpStatus.SC_MOVED_TEMPORARILY) {
					throw new DispatcherException("Failed to log in: " + status);
				}
			}
		} catch (ClientProtocolException e) {
			throw new DispatcherException("http protocol error", e);
		} catch (IOException e) {
			throw new DispatcherException(
					"connection problem/connection aborted", e);
		} catch (ParseException e) {
			throw new DispatcherException("failed to parse the login form", e);
		} catch (XPathExpressionException e) {
			throw new DispatcherException("failed to parse the login form", e);
		} catch (ParserConfigurationException e) {
			throw new DispatcherException("failed to parse the login form", e);
		} catch (SAXException e) {
			throw new DispatcherException("failed to parse the login form", e);
		} finally {
			// releases resources
			consumeResponseEntity(response);
		}

	}

	/**
	 * Gets the csrf token from the login form.
	 * 
	 * @param entity
	 *            HTTPEntity with the login form
	 * @return String with the csrf token or null in the case of problems
	 * @throws ParserConfigurationException
	 * @throws IOException
	 * @throws SAXException
	 * @throws ParseException
	 * @throws XPathExpressionException
	 */
	private String getCsrf(HttpEntity entity)
			throws ParserConfigurationException, ParseException, SAXException,
			IOException, XPathExpressionException {

		// gets a DOM builder factory
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

		// sets namespace awareness
		dbf.setNamespaceAware(false);

		// disables validation
		dbf.setValidating(false);
		dbf.setFeature(
				"http://apache.org/xml/features/nonvalidating/load-dtd-grammar",
				false);
		dbf.setFeature(
				"http://apache.org/xml/features/nonvalidating/load-external-dtd",
				false);

		// creates a new document builder from the factory
		DocumentBuilder builder = dbf.newDocumentBuilder();

		String entityContent = EntityUtils.toString(entity);
		
		// parses the response
		Document doc = builder.parse(new ByteArrayInputStream(entityContent.getBytes()));

		// gets a XPathFactory
		XPathFactory factory = XPathFactory.newInstance();

		// creates a new XPath
		XPath xpath = factory.newXPath();

		// compiles the XPath expression to get the csrf token
		XPathExpression expr = xpath
				.compile("//*[@name = 'csrfmiddlewaretoken']/@value");

		// evaluates the compiled XPath expression an returns the result
		return (String) expr.evaluate(doc, XPathConstants.STRING);

	}

	/**
	 * Ensures that the entity content is fully consumed and the content stream,
	 * if exists, is closed. This should be called at the end of each client
	 * request.
	 * 
	 * @param response
	 *            the HttpResponse that contains the entity.
	 */
	private void consumeResponseEntity(HttpResponse response) {

		try {
			if (response != null) {
				HttpEntity entity = response.getEntity();

				if (entity != null) {
					entity.consumeContent();
				}
			}
		} catch (IOException e) {
			// no need to propagate this exception because this method is always
			// called from a finally block
		}

	}

	/**
	 * Returns the base EATSML collection document.
	 * 
	 * @throws DispatcherException
	 *             in case of any failure.
	 */
	public Collection getBaseDocument() throws DispatcherException {

		try {
			// checks if the base document hasn't been requested before
			if (baseDoc == null) {
				// creates a new get request to get the base document
				HttpGet get = new HttpGet(serverUrl + BASE_DOCUMENT_URL);

				// executes the request and gets the response
				HttpResponse response = httpClient.execute(get, localContext);

				// checks the response is valid
				checkResponse(response);

				// gets the entity from the response
				baseDoc = EntityUtils.toString(response.getEntity(),
						DEFAULT_ENCODING);

				// converts the basedoc into a collection
				return DispatcherUtils.unmarshal(baseDoc);
			} else {
				// converts the current basedoc into a collection
				return DispatcherUtils.unmarshal(baseDoc);
			}
		} catch (ClientProtocolException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (ParseException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (IOException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (JAXBException e) {
			throw new DispatcherException(e.getMessage(), e);
		}

	}

	/**
	 * Checks that the response and the response entity are not null.
	 * 
	 * @param response
	 *            the HTTPResponse to check
	 * @throws DispatcherException
	 *             if the response or the response entity are null.
	 */
	private static void checkResponse(HttpResponse response)
			throws DispatcherException {

		if (response == null) {
			throw new DispatcherException("invalid response");
		}

		if (response.getEntity() == null) {
			throw new DispatcherException("invalid response entity");
		}

	}

	/**
	 * Returns a Collection with the results of looking up name on the EATS
	 * server.
	 * 
	 * @param name
	 *            string to search for.
	 * @return Collection
	 * @throws DispatcherException
	 */
	public Collection lookupName(String name) throws DispatcherException {

		// checks the given name
		if (name == null || name.length() < 1) {
			throw new DispatcherException("invalid lookup name");
		}

		try {
			// creates a new get request for the lookup name
			HttpGet get = new HttpGet(serverUrl + LOOKUP_NAME_URL + "?name="
					+ URLEncoder.encode(name, DEFAULT_ENCODING));

			// executes the request and gets the response
			HttpResponse response = httpClient.execute(get, localContext);

			// checks the response is valid
			checkResponse(response);

			// converts the response entity to a collection
			return DispatcherUtils.unmarshal(EntityUtils.toString(
					response.getEntity(), DEFAULT_ENCODING));
		} catch (ClientProtocolException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (ParseException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (IOException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (JAXBException e) {
			throw new DispatcherException(e.getMessage(), e);
		}

	}

	/**
	 * Returns the edit URL for the given entity.
	 * 
	 * @param entity
	 *            entity to get the URL.
	 * @return Edit URL, or null if the entity is invalid.
	 */
	public String getEditUrl(Entity entity) {

		if (entity == null) {
			return null;
		}

		return serverUrl + EDIT_ENTITY_PREFIX_URL + entity.getEatsId() + EDIT_ENTITY_SUFFIX_URL;

	}

	/**
	 * Imports a Collection into EATS and returns the URL of the resulting page.
	 * 
	 * @param c
	 *            collection to import.
	 * @param description
	 *            import description.
	 * @return URL of the page of the redirect.
	 * @throws DispatcherException
	 *             If the collection or the message are null, or if it failed to
	 *             import.
	 */
	public String importDocument(Collection c, String description)
			throws DispatcherException {

		if (c == null) {
			throw new DispatcherException("invalid collection");
		}

		if (description == null || description.length() < 1) {
			throw new DispatcherException("invalid description");
		}

		HttpResponse response = null;
		File file = null;

		try {
			if (csrfToken == null || csrfToken.isEmpty()) {
				// creates a new get request to get the login form
				HttpGet get = new HttpGet(serverUrl + IMPORT_URL);
				get.setParams(httpParams);

				// executes the get request
				response = httpClient.execute(get, localContext);

				if (response != null && response.getEntity() != null) {
					// gets the crsf token
					csrfToken = getCsrf(response.getEntity());
				}
			}
			
			// creates a new temporary file to save the given collection
			file = File.createTempFile("eats", ".xml");

			// creates a file writer for the temporary file
			FileOutputStream fos = new FileOutputStream(file);

			// writes the collection into the file
			fos.write(DispatcherUtils.marshall(c).getBytes(DEFAULT_ENCODING));

			// releases file writer resources
			fos.flush();
			fos.close();

			// creates a new post request to upload the file
			HttpPost post = new HttpPost(serverUrl + IMPORT_URL);
			post.addHeader("Referer", serverUrl + IMPORT_URL);

			// creates a new multipart entity to set the post parameters
			MultipartEntity entity = new MultipartEntity();
			entity.addPart("import_file", new FileBody(file, "text/xml"));
			entity.addPart("description", new StringBody(description));
			entity.addPart("csrfmiddlewaretoken", new StringBody(csrfToken));

			// sets the post parameters
			post.setEntity(entity);

			// imports the collection and gets the response
			response = httpClient.execute(post, localContext);

			// checks the response is valid
			checkResponse(response);

			// if the import was successful it will return a redirect response
			// code
			if (response.getStatusLine().getStatusCode() != 302) {
				throw new DispatcherException("Failed to import");
			}

			// returns the redirection url
			return response.getFirstHeader("Location").getValue();
		} catch (UnsupportedEncodingException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (ClientProtocolException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (JAXBException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (IOException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (ParseException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (XPathExpressionException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (ParserConfigurationException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (SAXException e) {
			throw new DispatcherException(e.getMessage(), e);
		} finally {
			// releases resources
			consumeResponseEntity(response);

			// removes the temporary file
			file.delete();
		}

	}

	/**
	 * Returns a Collection representing the processed import.
	 * 
	 * @param url
	 *            URL for the import
	 * @return Collection
	 * @throws DispatcherException
	 */
	public Collection getProcessedImport(String url) throws DispatcherException {

		if (url == null || url.length() < 1) {
			throw new DispatcherException("Invalid URL");
		}

		try {
			// creates a new get request
			HttpGet get = new HttpGet(url + PROCESSED_IMPORT_URL);

			// executes the processed import request
			HttpResponse response = httpClient.execute(get, localContext);

			// checks the response is valid
			checkResponse(response);

			// converts the response entity into a collection
			return DispatcherUtils.unmarshal(EntityUtils.toString(
					response.getEntity(), DEFAULT_ENCODING));
		} catch (ClientProtocolException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (ParseException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (IOException e) {
			throw new DispatcherException(e.getMessage(), e);
		} catch (JAXBException e) {
			throw new DispatcherException(e.getMessage(), e);
		}

	}

}
