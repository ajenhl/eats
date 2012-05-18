/**
 * LookupPreferencesMain.java
 * Oct 5, 2010
 */
package uk.ac.kcl.cch.eats.lookup;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

/**
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 *
 */
public class LookupPreferencesControllerMain {

    /**
     * @param args
     */
    public static void main(String[] args) {
        LookupPreferencesController lp = LookupPreferencesController.getInstance((JFrame) SwingUtilities.getRoot(null));
        lp.showDialog();
    }

}
