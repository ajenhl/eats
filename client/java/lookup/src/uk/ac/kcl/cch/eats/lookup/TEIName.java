/**
 * TEIName.java
 * Sep 30, 2010
 */
package uk.ac.kcl.cch.eats.lookup;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.StringWriter;
import java.io.UnsupportedEncodingException;
import java.util.Hashtable;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Result;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

/**
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 */
public class TEIName {

    public static final String XML_ENCODING_UTF_8 = "UTF-8";

    public static final String TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0";

    private String teiPrefix = null;

    private String nameString = null;

    private Element nameElement = null;

    private String xsltPath = null;

    // Contructor(s)

    public TEIName() {

    }

    public TEIName(String name, Hashtable<String, String> nsHash, String xsltPath)
            throws TEINameException {
        this.xsltPath = xsltPath;

        TEIName teiName = cleanName(name, nsHash);

        nameString = teiName.nameString;
        nameElement = teiName.nameElement;
    }

    // Method(s)

    /**
     * Returns a TEIName with a name without any markup, and a name with
     * surrounding name markup as an XML element node.
     * 
     * @param name
     *            the name
     * @return TEIName
     * @throws TEINameException
     */
    private TEIName cleanName(String name, Hashtable<String, String> nsHash)
            throws TEINameException {

        teiPrefix = nsHash.get(TEI_NAMESPACE);

        if (teiPrefix != null && teiPrefix.length() > 0) {
            teiPrefix += ":";
        } else {
            teiPrefix = "";
        }

        String elName = teiPrefix + "name";

        // Parse name as XML, to make it easier to deal with (and since it comes
        // from an XML document).
        String nameAsXml = "<" + elName;

        if (nsHash != null && nsHash.size() > 0) {
            for (Object uri : nsHash.keySet().toArray()) {
                String prefix = nsHash.get(uri);

                if (prefix != null && prefix.length() > 0) {
                    nameAsXml += " xmlns:" + prefix + "=\"" + uri + "\"";
                } else {
                    nameAsXml += " xmlns=\"" + uri + "\"";
                }
            }
        }

        nameAsXml = nameAsXml.trim();
        nameAsXml += ">" + name + "</" + elName + ">";

        // converts from TEI specific names to generic name element with
        // additional attributes
        nameAsXml = transform(nameAsXml, new File(xsltPath,
                "convert_from_specific_name_elements.xsl"));

        Document doc = getXmlFromString(nameAsXml);

        Element root = doc.getDocumentElement();

        String nameString = root.getTextContent().trim();

        // Determine whether the original name is wrapped in a single
        // name element. If it is, then create an XML representation
        // without a second enclosing name element, and strip all
        // attributes from the name element.
        NodeList children = root.getChildNodes();

        if (children.getLength() == 1) {
            String nodeName = children.item(0).getNodeName();

            // this shouldn't be necessary, but getLocalName() is returning null
            if (nodeName.indexOf(":") > 0) {
                nodeName = nodeName.substring(nodeName.indexOf(":") + 1);
            }

            if (nodeName.equals("name")) {
                root = (Element) children.item(0);
            }
        }

        TEIName teiName = new TEIName();
        teiName.nameString = nameString;
        teiName.nameElement = root;

        return teiName;

    }

    /**
     * Transforms the given XML string using the XSLT at the given location.
     * 
     * @param input
     *            XML string
     * @param xslt
     *            XSLT file
     * @return XML string
     */
    private String transform(String input, File xslt) throws TEINameException {

        String message = "Could not transform XML string using: " + xslt;

        try {
            // gets a new transformer factory to create the transformers
            TransformerFactory factory = TransformerFactory.newInstance();

            // creates a new transformer for the xslt
            Transformer transformer = factory.newTransformer(new StreamSource(new FileInputStream(
                    xslt)));

            ByteArrayOutputStream output = new ByteArrayOutputStream();

            transformer.transform(new StreamSource(new ByteArrayInputStream(input
                    .getBytes(XML_ENCODING_UTF_8))), new StreamResult(output));

            return output.toString(XML_ENCODING_UTF_8);
        } catch (TransformerConfigurationException e) {
            throw new TEINameException(message, e);
        } catch (FileNotFoundException e) {
            throw new TEINameException(message, e);
        } catch (UnsupportedEncodingException e) {
            throw new TEINameException(message, e);
        } catch (TransformerFactoryConfigurationError e) {
            throw new TEINameException(message, e.getException());
        } catch (TransformerException e) {
            throw new TEINameException(message, e);
        }

    }

    /**
     * Creates a DOM document from the string.
     * 
     * @param string
     *            the string
     * @return DOM document
     * @throws TEINameException
     */
    private Document getXmlFromString(String string) throws TEINameException {

        String message = "Could not parse string as XML.";

        try {
            ByteArrayInputStream is = new ByteArrayInputStream(string.trim().getBytes(
                    XML_ENCODING_UTF_8));

            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();

            DocumentBuilder builder = factory.newDocumentBuilder();

            Document root = builder.parse(is);

            return root;
        } catch (UnsupportedEncodingException e) {
            throw new TEINameException(message, e);
        } catch (ParserConfigurationException e) {
            throw new TEINameException(message, e);
        } catch (SAXException e) {
            throw new TEINameException(message, e);
        } catch (IOException e) {
            throw new TEINameException(message, e);
        }

    }

    /**
     * Sets the ref attribute in the XML to ref.
     * 
     * @param ref
     *            the ref
     */
    public void setRef(String ref) {
        nameElement.setAttribute("ref", ref);
    }

    /**
     * Sets the type attribute in the XML to type.
     * 
     * @param type
     *            the type
     */
    public void setType(String type) {
        nameElement.setAttribute("type", type);
    }

    /**
     * Return the XML name serialised as a string.
     * 
     * @return String
     * @throws TEINameException
     */
    public String getXmlName() throws TEINameException {

        String message = "Failed to serialize name as TEI.";

        try {
            TransformerFactory factory = TransformerFactory.newInstance();

            Transformer transformer = factory.newTransformer();
            transformer.setOutputProperty("omit-xml-declaration", "yes");
            transformer.setOutputProperty("encoding", XML_ENCODING_UTF_8);

            StringWriter writer = new StringWriter();

            Source source = new DOMSource(nameElement);

            Result result = new StreamResult(writer);

            transformer.transform(source, result);

            String xml = writer.toString();

            xml = transform(xml, new File(xsltPath, "convert_to_specific_name_elements.xsl"));

            xml = xml.replaceAll(" xmlns(:[^=]+)?=[\"\'][^\"\']+[\"\']", "");

            if (xml.indexOf(teiPrefix) != 1) {
                xml = xml.replaceFirst("<", "<" + teiPrefix);

                int pos = xml.lastIndexOf("<") + 2;

                xml = xml.substring(0, pos) + teiPrefix + xml.substring(pos);
            }

            return xml;
        } catch (TransformerConfigurationException e) {
            throw new TEINameException(message, e);
        } catch (IllegalArgumentException e) {
            throw new TEINameException(message, e);
        } catch (TransformerFactoryConfigurationError e) {
            throw new TEINameException(message, e.getException());
        } catch (TransformerException e) {
            throw new TEINameException(message, e);
        }

    }

    // Internal Classes

    public class TEINameException extends Exception {
        private static final long serialVersionUID = 6148882914128613827L;

        public TEINameException(String message) {
            super(message);
        }

        public TEINameException(String message, Exception e) {
            super(message, e);
        }
    }

    // Getter(s) and Setter(s)

    /**
     * @return the nameString
     */
    public String getNameString() {
        return normaliseChars(normaliseSpace(nameString));
    }

    /**
     * Return name with spaces properly normalised. Replace all whitespace
     * characters with spaces.
     * 
     * @param name
     *            the name
     * @return String
     */
    private String normaliseSpace(String name) {

        // This handles newlines (cross-platform), tabs, etc.
        name = name.replaceAll("\\s", " ");
        // Remove leading and trailing whitespace.
        name = name.trim();
        // Reduce all consecutive spaces to a single space.
        name = name.replaceAll(" {2,}", " ");

        return name;

    }

    /**
     * Return name with ASCII punctuation characters normalised to Unicode
     * characters.
     * 
     * @param name
     *            the name
     * @return String
     */
    private String normaliseChars(String name) {

        // Translate ASCII apostrophe to Unicode apostrophe.
        name = name.replace("'", "\u2019");

        return name;

    }

}
