/**
 * LookupPreferences.java
 * Oct 6, 2010
 */
package uk.ac.kcl.cch.eats.lookup;

import java.util.prefs.BackingStoreException;
import java.util.prefs.Preferences;

import uk.ac.kcl.cch.eats.dispatcher.Dispatcher;
import uk.ac.kcl.cch.eats.dispatcher.DispatcherException;

/**
 * Class to store preferences for the look up.
 * 
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 */
public class LookupPreferences {

	/**
	 * EATS server URL.
	 */
	private String url = null;
	private static final String URL_KEY = "url";
	private static final String URL_DEFAULT = "http://";

	/**
	 * EATS server username.
	 */
	private String username = null;
	private static final String USERNAME_KEY = "username";
	private static final String USERNAME_DEFAULT = "";

	/**
	 * EATS server password.
	 */
	private String password = null;
	private static final String PASSWORD_KEY = "password";
	private static final String PASSWORD_DEFAULT = "";

	/**
	 * Remote proxy username.
	 */
	private String proxyUsername = null;
	private static final String PROXY_USERNAME_KEY = "proxy.username";
	private static final String PROXY_USERNAME_DEFAULT = "";

	/**
	 * Remote proxy password.
	 */
	private String proxyPassword = null;
	private static final String PROXY_PASSWORD_KEY = "proxy.password";
	private static final String PROXY_PASSWORD_DEFAULT = "";
        
        /**
         * Reference Tool URL.
         */
        private String refsUrl = null;
        private static final String REFS_URL_KEY = "refsUrl";
        private static final String REFS_URL_DEFAULT = "";
        
        /**
         * Auto edit in browser checkbox.
         */
        private Boolean isAutoEditInBrowser = null;
        private static final String AUTO_EDIT_IN_BROWSER_KEY = "autoEditInBrowser";
        private static final Boolean AUTO_EDIT_IN_BROWSER_DEFAULT = false;

	/**
     * 
     */
	public LookupPreferences() {

		load();

	}

	/**
	 * Loads the preferences from the Preferences object.
	 */
	private void load() {

		Preferences preferences = Preferences.userNodeForPackage(getClass());
		setUrl(preferences.get(URL_KEY, URL_DEFAULT));
		setUsername(preferences.get(USERNAME_KEY, USERNAME_DEFAULT));
		setPassword(preferences.get(PASSWORD_KEY, PASSWORD_DEFAULT));
		setProxyUsername(preferences.get(PROXY_USERNAME_KEY,
				PROXY_USERNAME_DEFAULT));
		setProxyPassword(preferences.get(PROXY_PASSWORD_KEY,
				PROXY_PASSWORD_DEFAULT));
                setRefsUrl(preferences.get(REFS_URL_KEY, REFS_URL_DEFAULT));
                setAutoEditInBrowser(preferences.getBoolean(AUTO_EDIT_IN_BROWSER_KEY,
                        AUTO_EDIT_IN_BROWSER_DEFAULT));

	}

	/**
	 * Saves the LookupPreferences.
	 * 
	 * @throws BackingStoreException
	 */
	public void save() throws BackingStoreException {

		Preferences preferences = Preferences.userNodeForPackage(getClass());
		preferences.put(URL_KEY, (getUrl() != null ? getUrl() : URL_DEFAULT));
		preferences.put(USERNAME_KEY, (getUsername() != null ? getUsername()
				: USERNAME_DEFAULT));
		preferences.put(PASSWORD_KEY, (getPassword() != null ? getPassword()
				: PASSWORD_DEFAULT));
		preferences.put(PROXY_USERNAME_KEY,
				(getProxyUsername() != null ? getProxyUsername()
						: PROXY_USERNAME_DEFAULT));
		preferences.put(PROXY_PASSWORD_KEY,
				(getProxyPassword() != null ? getProxyPassword()
						: PROXY_PASSWORD_DEFAULT));
                preferences.put(REFS_URL_KEY, (getRefsUrl() != null ? getRefsUrl()
                        : REFS_URL_DEFAULT));
                preferences.putBoolean(AUTO_EDIT_IN_BROWSER_KEY,
                        (getAutoEditInBrowser() != null ? getAutoEditInBrowser() :
                                AUTO_EDIT_IN_BROWSER_DEFAULT));
		preferences.flush();

	}

	/**
	 * Creates and returns a dispatcher using the properties.
	 * 
	 * @return Dispatcher
	 * @throws DispatcherException
	 */
	public Dispatcher getDispatcher() {
		return new Dispatcher(getUrl(), getUsername(), getPassword(),
				getProxyUsername(), getProxyPassword());
	}

	/**
	 * @return the url
	 */
	public String getUrl() {
		return url;
	}

	/**
	 * @param url
	 *            the url to set
	 */
	public void setUrl(String url) {
		this.url = url;
	}

	/**
	 * @return the username
	 */
	public String getUsername() {
		return username;
	}

	/**
	 * @param username
	 *            the username to set
	 */
	public void setUsername(String username) {
		this.username = username;
	}

	/**
	 * @return the password
	 */
	public String getPassword() {
		return password;
	}

	/**
	 * @param password
	 *            the password to set
	 */
	public void setPassword(String password) {
		this.password = password;
	}

	/**
	 * @return the proxyUsername
	 */
	public String getProxyUsername() {
		return proxyUsername;
	}

	/**
	 * @param proxyUsername
	 *            the proxyUsername to set
	 */
	public void setProxyUsername(String proxyUsername) {
		this.proxyUsername = proxyUsername;
	}

	/**
	 * @return the proxyPassword
	 */
	public String getProxyPassword() {
		return proxyPassword;
	}

	/**
	 * @param proxyPassword
	 *            the proxyPassword to set
	 */
	public void setProxyPassword(String proxyPassword) {
		this.proxyPassword = proxyPassword;
	}
        
        /**
         * @return the refsUrl
         */
        public String getRefsUrl() {
            return refsUrl;
        }
        
        /**
         * @param refsUrl the refsUrl to set
         */
        public void setRefsUrl(String refsUrl) {
            this.refsUrl = refsUrl;
        }
        
        public Boolean getAutoEditInBrowser() {
            return this.isAutoEditInBrowser;
        }
        
        public void setAutoEditInBrowser(Boolean isSelected) {
            this.isAutoEditInBrowser = isSelected;
        }

}
