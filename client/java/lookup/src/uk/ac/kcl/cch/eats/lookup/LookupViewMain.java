/**
 * LookupViewMain.java
 * Sep 14, 2010
 */
package uk.ac.kcl.cch.eats.lookup;


/**
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 * 
 */
public class LookupViewMain {

	public static void main(String[] args) {
		javax.swing.SwingUtilities.invokeLater(new Runnable() {
			public void run() {
				new LookupView().setVisible(true);
			}
		});
	}

}
