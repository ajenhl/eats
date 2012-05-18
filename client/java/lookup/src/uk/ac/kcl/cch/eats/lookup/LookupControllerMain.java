/**
 * LookupControllerMain.java
 * Sep 15, 2010
 */
package uk.ac.kcl.cch.eats.lookup;

import java.io.File;
import java.util.Hashtable;

import uk.ac.kcl.cch.eats.dispatcher.DispatcherException;
import uk.ac.kcl.cch.eats.lookup.TEIName.TEINameException;

/**
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 * 
 */
public class LookupControllerMain {

	/**
	 * @param args
	 * @throws DispatcherException
	 * @throws TEINameException
	 */
	public static void main(String[] args) throws DispatcherException,
			TEINameException {

		LookupPreferencesController lookupPreferencesController = LookupPreferencesController
				.getInstance(null);

		if (!lookupPreferencesController.isPreferencesSet()) {
			lookupPreferencesController.showDialog();

			if (!lookupPreferencesController.isPreferencesSet()) {
				System.exit(-1);
			}
		}

		LookupController lc = new LookupController(lookupPreferencesController);
		lc.showView(new TEIName("george",
				new Hashtable<String, String>(), new File("").getAbsolutePath()
						+ "/etc/xslt").getNameString(), "person");
	}

}
