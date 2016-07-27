/**
 * LookupPluginExtension.java
 * Sep 28, 2010
 */
package uk.ac.kcl.cch.eats.lookup.plugin.oxygen;

import java.util.Hashtable;

import javax.swing.JOptionPane;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

import ro.sync.exml.plugin.selection.SelectionPluginContext;
import ro.sync.exml.plugin.selection.SelectionPluginExtension;
import ro.sync.exml.plugin.selection.SelectionPluginResult;
import ro.sync.exml.plugin.selection.SelectionPluginResultImpl;
import uk.ac.kcl.cch.eats.lookup.LookupController;
import uk.ac.kcl.cch.eats.lookup.LookupPreferencesController;
import uk.ac.kcl.cch.eats.lookup.TEIName;

/**
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 * 
 */
public class LookupPluginExtension extends DefaultHandler implements
		SelectionPluginExtension {

	private Hashtable<String, String> nsHash = null;

	/**
	 * 
	 * @see ro.sync.exml.plugin.selection.SelectionPluginExtension#process(ro.sync.exml.plugin.selection.SelectionPluginContext)
	 */
	@Override
	public SelectionPluginResult process(SelectionPluginContext context) {

		String jarPath = getClass().getProtectionDomain().getCodeSource()
				.getLocation().getPath();
		jarPath = jarPath.substring(0, jarPath.lastIndexOf("/"));

		String xsltPath = jarPath + "/xslt";

		LookupPreferencesController lookupPreferencesController = 
				LookupPreferencesController.getInstance(context.getFrame());

		nsHash = new Hashtable<String, String>();

		// From oXygen support:
		// This is necessary because the method is called from the AWT thread
		// when the action is invoked by the user so we have to switch the 
		// class loader to the one which was used to load the extension and
		// which should use the other Saxon library
		ClassLoader cl = Thread.currentThread().getContextClassLoader();
		Thread.currentThread().setContextClassLoader(
				LookupPluginExtension.this.getClass().getClassLoader());

		try {
			SAXParserFactory factory = SAXParserFactory.newInstance();
			factory.setNamespaceAware(true);

			SAXParser parser = factory.newSAXParser();
			parser.parse(context.getDocumentURL().openStream(), this);

			if (!lookupPreferencesController.isPreferencesSet()) {
				lookupPreferencesController.showDialog();

				if (!lookupPreferencesController.isPreferencesSet()) {
					return null;
				}
			}

			TEIName teiName = new TEIName(context.getSelection(), nsHash,
					xsltPath);

			LookupController lookupController = LookupPlugin
					.getLookupController(context.getFrame(),
							lookupPreferencesController);

			lookupController.showView(teiName.getNameString(), "person");

			String ref = lookupController.getRef();

			if (ref != null && ref.length() > 0) {
				teiName.setRef(ref);

				String type = lookupController.getType();

				if (type != null && type.length() > 0) {
					teiName.setType(type);
				}

				return new SelectionPluginResultImpl(teiName.getXmlName());
			}

			return new SelectionPluginResultImpl(context.getSelection());
		} catch (Exception e) {
			lookupPreferencesController.setPreferencesSet(false);

			e.printStackTrace();

			JOptionPane.showMessageDialog(context.getFrame(), e.getMessage(),
					"Exception", JOptionPane.ERROR_MESSAGE);
		} finally {
			Thread.currentThread().setContextClassLoader(cl);
		}

		return null;

	}

	/**
	 * Collects all the namespaces in the current XML document.
	 * 
	 * @see org.xml.sax.helpers.DefaultHandler#startPrefixMapping(java.lang.String,
	 *      java.lang.String)
	 */
	@Override
	public void startPrefixMapping(String prefix, String uri)
			throws SAXException {
		nsHash.put(uri, prefix);
	}

}
