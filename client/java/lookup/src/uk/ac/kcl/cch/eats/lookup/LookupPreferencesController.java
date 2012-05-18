/**
 * LookupPreferences.java
 * Oct 5, 2010
 */
package uk.ac.kcl.cch.eats.lookup;

import java.awt.Frame;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.prefs.BackingStoreException;

import javax.swing.JOptionPane;

/**
 * Controller class for the lookup preferences.
 * 
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 */
public class LookupPreferencesController implements ActionListener {

	/**
	 * Keeps a copy of itself to make sure it is only created once.
	 */
	private static LookupPreferencesController instance = null;

	/**
	 * LookupPreferences.
	 */
	private LookupPreferences lookupPreferences = null;

	/**
	 * Dialog window.
	 */
	private LookupPreferencesDialog dialog = null;

	/**
	 * Flag to indicate is the preferences were set.
	 */
	private boolean preferencesSet = false;

	/**
	 * Creates new LookupPreferences
	 */
	private LookupPreferencesController(Frame frame) {

		dialog = new LookupPreferencesDialog(frame, true);

		lookupPreferences = new LookupPreferences();

		initDialog();

	}

	/**
	 * Gets a new LookupPreferences instance.
	 * 
	 * @return LookupPreferences
	 */
	public static LookupPreferencesController getInstance(Frame frame) {

		if (instance == null) {
			instance = new LookupPreferencesController(frame);
		}

		return instance;

	}

	/**
	 * Initializes the dialog components.
	 */
	private void initDialog() {

		dialog.jUrlTextField.setText(lookupPreferences.getUrl());
		dialog.jUsernameTextField.setText(lookupPreferences.getUsername());
		dialog.jPasswordTextField.setText(lookupPreferences.getPassword());
		dialog.jProxyUsernameTextField.setText(lookupPreferences
				.getProxyUsername());
		dialog.jProxyPasswordField
				.setText(lookupPreferences.getProxyPassword());

		dialog.getRootPane().setDefaultButton(dialog.jOkButton);

		dialog.jCancelButton.addActionListener(this);
		dialog.jOkButton.addActionListener(this);

	}

	/**
	 * Listener method that deals with events from the dialog buttons.
	 * 
	 * @see java.awt.event.ActionListener#actionPerformed(java.awt.event.ActionEvent)
	 */
	@Override
	public void actionPerformed(ActionEvent e) {

		if (e.getSource().equals(dialog.jCancelButton)) {
			preferencesSet = false;

			closeDialog();
		} else if (e.getSource().equals(dialog.jOkButton)) {
			lookupPreferences.setUrl(dialog.jUrlTextField.getText().trim());
			lookupPreferences.setUsername(dialog.jUsernameTextField.getText()
					.trim());
			lookupPreferences.setPassword(new String(dialog.jPasswordTextField
					.getPassword()).trim());
			lookupPreferences.setProxyUsername(dialog.jProxyUsernameTextField
					.getText().trim());
			lookupPreferences.setProxyPassword(new String(
					dialog.jProxyPasswordField.getPassword()).trim());

			try {
				lookupPreferences.save();
			} catch (BackingStoreException ex) {
				JOptionPane.showMessageDialog(dialog, ex.getMessage(),
						"Exception", JOptionPane.ERROR_MESSAGE);
			}

			preferencesSet = true;

			closeDialog();
		}

	}

	/**
	 * Closes the dialog window and frees resources.
	 */
	private void closeDialog() {
		dialog.setVisible(false);
	}

	/**
	 * Displays the dialog window.
	 */
	public void showDialog() {
		dialog.setVisible(true);
	}

	/**
	 * @return the lookupPreferences
	 */
	public LookupPreferences getLookupPreferences() {
		return lookupPreferences;
	}

	/**
	 * @return the preferencesSet
	 */
	public boolean isPreferencesSet() {
		return preferencesSet;
	}

	/**
	 * @param preferencesSet
	 *            the preferencesSet to set
	 */
	public void setPreferencesSet(boolean preferencesSet) {
		this.preferencesSet = preferencesSet;
	}

}
