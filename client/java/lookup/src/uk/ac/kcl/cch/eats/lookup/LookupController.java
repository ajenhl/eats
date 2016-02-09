/**
 * LookupModel.java
 * Sep 13, 2010
 */
package uk.ac.kcl.cch.eats.lookup;

import java.awt.Cursor;
import java.awt.Desktop;
import java.awt.Font;
import java.awt.Frame;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Hashtable;
import java.util.List;

import javax.swing.AbstractAction;
import javax.swing.GroupLayout;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.JTextPane;
import javax.swing.KeyStroke;
import javax.swing.GroupLayout.Alignment;
import javax.swing.GroupLayout.Group;
import javax.swing.GroupLayout.ParallelGroup;
import javax.swing.GroupLayout.SequentialGroup;
import javax.swing.LayoutStyle.ComponentPlacement;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.event.HyperlinkEvent;
import javax.swing.event.HyperlinkListener;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableColumn;

import uk.ac.kcl.cch.eats.dispatcher.Dispatcher;
import uk.ac.kcl.cch.eats.dispatcher.DispatcherException;
import nz.org.artefact.eats.ns.eatsml.Authority;
import nz.org.artefact.eats.ns.eatsml.Collection;
import nz.org.artefact.eats.ns.eatsml.Collection.EntityTypes.EntityType;
import nz.org.artefact.eats.ns.eatsml.Date;
import nz.org.artefact.eats.ns.eatsml.Entities;
import nz.org.artefact.eats.ns.eatsml.Entity;
import nz.org.artefact.eats.ns.eatsml.EntityRelationship;
import nz.org.artefact.eats.ns.eatsml.EntityRelationships;
import nz.org.artefact.eats.ns.eatsml.Languages.Language;
import nz.org.artefact.eats.ns.eatsml.NamePart;
import nz.org.artefact.eats.ns.eatsml.NamePartTypes.NamePartType;
import nz.org.artefact.eats.ns.eatsml.NameTypes.NameType;
import nz.org.artefact.eats.ns.eatsml.Names;
import nz.org.artefact.eats.ns.eatsml.Names.Name;
import nz.org.artefact.eats.ns.eatsml.Entity.Notes.Note;
import nz.org.artefact.eats.ns.eatsml.Scripts.Script;
import nz.org.artefact.eats.ns.eatsml.ext.EatsMlUtils;

/**
 * This class serves as an interface between the eatsml library and the plugins.
 * 
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 */
public class LookupController implements ActionListener, DocumentListener,
		ListSelectionListener, HyperlinkListener {

	/**
	 * Column used to store the Entity object.
	 */
	private static final int ENTITY_COLUMN = 0;

	/**
	 * Column for the Entity details.
	 */
	private static final int ENTITY_DETAILS_COLUMN = 1;

	/**
	 * Column for the Entity type.
	 */
	private static final int ENTITY_TYPE_COLUMN = 2;

	/**
	 * Number of columns without the name part type columns.
	 */
	private static final int BASE_COLUMN_COUNT = 3;

	// Properties

	/**
	 * Look up preferences.
	 */
	private LookupPreferencesController preferences = null;

	/**
	 * EATS server dispatcher.
	 */
	private Dispatcher dispatcher = null;

	/**
	 * Default Authority.
	 */
	private Authority authority = null;

	/**
	 * The lookup view.
	 */
	private LookupView view = null;

	/**
	 * JTable that holds the results from EATS.
	 */
	private JTable table = null;

	/**
	 * Collection where all the search results are stored.
	 */
	private Collection searchResults = null;

	/**
	 * Key of the selected entity.
	 */
	private String key = null;

	/**
	 * Type of the selected entity.
	 */
	private String type = null;

	/**
	 * Hashtable with the name part types with corresponding JTextFields.
	 */
	private Hashtable<NamePartType, JTextField> namePartTypesTextFieldsHash = null;

	/**
	 * Hashtable with the name part types with corresponding table columns.
	 */
	private Hashtable<String, Integer> namePartTypesColumnsHash = null;

	/**
	 * List that stores all the dynamic text fields that are created for the
	 * name part types.
	 */
	private ArrayList<JTextField> texts = null;

	private Frame parent = null;
	private String viewTitle = null;
	private boolean viewModality = false;
	private String lookupName = null;
	private String lookupType = null;

	// Constructo(r)

	/**
	 * Creates a new LookupController.
	 * 
	 * @param preferences
	 *            the Dispatcher
	 */
	public LookupController(LookupPreferencesController preferences) {
		this.preferences = preferences;

		dispatcher = preferences.getLookupPreferences().getDispatcher();

		view = new LookupView();
		table = view.resultsTable;

		initView();
	}

	/**
	 * Creates a new LookupController.
	 * 
	 * @param preferences
	 *            the Dispatcher
	 * @param frame
	 *            parent Frame
	 * @param title
	 *            the window title
	 * @param modal
	 *            True if the window should be modal
	 */
	public LookupController(LookupPreferencesController preferences,
			Frame parent, String viewTitle, boolean viewModality) {
		this.preferences = preferences;
		this.parent = parent;
		this.viewTitle = viewTitle;
		this.viewModality = viewModality;

		dispatcher = preferences.getLookupPreferences().getDispatcher();

		view = new LookupView(parent, viewTitle, viewModality);
		table = view.resultsTable;

		initView();
	}

	// Methods

	/**
	 * Configures the view with information from the dispatcher.
	 */
	public void initView() {

		try {
			waitCursor();

			dispatcher.login();

			// gets the base document from the EATS server
			Collection baseDocument = dispatcher.getBaseDocument();

			view.setAlwaysOnTop(false);

			// sets the find button as the form default button
			view.getRootPane().setDefaultButton(view.findButton);

			// adds action listeners to the JButtons
			view.preferencesButton.addActionListener(this);
			view.cancelButton.addActionListener(this);
			view.newButton.addActionListener(this);
			view.findButton.addActionListener(this);
			view.editButton.addActionListener(this);
			view.editButton.setEnabled(false);

			// adds a document listener to the display name JTextField
			view.displayNameText.getDocument().addDocumentListener(this);

			// authority
			authority = EatsMlUtils.getDefaultAuthority(baseDocument);
			view.authorityText.setText(authority.getName());

			// Populate the Combo boxes with the items associated with authority.
			this.populateEntityTypes(authority);
			this.populateLanguages(authority);
			this.populateScripts(authority);
			this.populateNameTypes(authority);

			// sets table ordering
			table.setAutoCreateRowSorter(true);
			// increases the row height
			table.setRowHeight(table.getRowHeight() * 2);
			// adds a listener to display the entity details
			table.getSelectionModel().addListSelectionListener(this);

			// adds a mouse listener to listen for double-click events
			table.addMouseListener(new MouseAdapter() {
				@Override
				public void mouseClicked(MouseEvent e) {
					super.mouseClicked(e);

					// double click
					if (e.getClickCount() == 2) {
						setKeyAndType(null);
						closeWindow();
					}
				}
			});

			// adds a key listener to listen for Enter key
			table.getInputMap().put(
					KeyStroke.getKeyStroke(KeyEvent.VK_ENTER, 0), "setKey");
			table.getActionMap().put("setKey", new AbstractAction() {
				private static final long serialVersionUID = -3200639298072014965L;

				@Override
				public void actionPerformed(ActionEvent e) {
					setKeyAndType(null);
					closeWindow();
				}
			});
			
			this.generateNamePartTypes((Language) ((ComboObjectHolder<Language>) view.languageCombo.getSelectedItem()).getObject());
			// hides the entity column
			TableColumn tc = table.getColumnModel().getColumn(ENTITY_COLUMN);
			table.getColumnModel().removeColumn(tc);
			table.sizeColumnsToFit(-1);

			// adds hyperlink listener to the textpane
			view.detailsTextPane.addHyperlinkListener(this);
		} catch (DispatcherException e) {
			showExceptionDialog(e);
		} finally {
			defaultCursor();
		}

	}
	
	/**
	 * Creates fields for the name part types associated with language.
	 * 
	 * @param language
	 */
	private void generateNamePartTypes(Language language) {
		Language.NamePartTypes languageNPT = language.getNamePartTypes();
		List<NamePartType> nptList = new ArrayList<NamePartType>();
		if (languageNPT != null) {
			for (Language.NamePartTypes.NamePartType npt : languageNPT.getNamePartType()) {
				NamePartType namePartType = (NamePartType) npt.getRef();
				nptList.add(namePartType);
			}

			GroupLayout layout = new GroupLayout(view.dynFormPanel);
			view.dynFormPanel.setLayout(layout);

			ParallelGroup horizontalGroup = layout
					.createParallelGroup(Alignment.LEADING);
			SequentialGroup verticalGroup = layout.createSequentialGroup();

			ArrayList<JLabel> labels = new ArrayList<JLabel>();
			texts = new ArrayList<JTextField>();

			namePartTypesTextFieldsHash = new Hashtable<NamePartType, JTextField>();
			namePartTypesColumnsHash = new Hashtable<String, Integer>();

			DefaultTableModel model = (DefaultTableModel) table.getModel();

			int column = BASE_COLUMN_COUNT;

			for (NamePartType npt : nptList) {
				namePartTypesColumnsHash.put(npt.getId(), column++);

				String name = Character.toTitleCase(npt.getName()
						.charAt(0)) + npt.getName().substring(1);
				JLabel label = new JLabel();
				label.setText(name + ":");

				labels.add(label);

				JTextField text = new JTextField();

				texts.add(text);

				namePartTypesTextFieldsHash.put(npt, text);

				verticalGroup
					.addGroup(
							layout.createParallelGroup(
									Alignment.BASELINE)
									.addComponent(label)
									.addComponent(text))
							.addPreferredGap(ComponentPlacement.UNRELATED);

				model.addColumn(name);
			}

			Group group = layout.createSequentialGroup().addContainerGap();
			Group labelsGroup = layout
					.createParallelGroup(Alignment.LEADING);

			for (JLabel l : labels) {
				labelsGroup.addComponent(l);
			}

			group.addGroup(labelsGroup);
			group.addGap(2);

			Group textsGroup = layout
					.createParallelGroup(Alignment.LEADING);

			for (JTextField t : texts) {
				t.getDocument().addDocumentListener(this);
				textsGroup.addComponent(t);
			}

			group.addGroup(textsGroup);
			horizontalGroup.addGroup(group);
			layout.setHorizontalGroup(horizontalGroup);
			layout.setVerticalGroup(verticalGroup);
		}		
	}
	
	/**
	 * Sets the entity types in the entityTypeCombo to those associated with authority.
	 * 
	 * @param authority
	 */
	private void populateEntityTypes(Authority authority) {
		view.entityTypeCombo.removeAllItems();
		List<EntityType> etList = new ArrayList<EntityType>();
		Authority.EntityTypes authorityEntityTypes = authority.getEntityTypes();
		if (authorityEntityTypes != null) {
			for (Authority.EntityTypes.EntityType t : authorityEntityTypes.getEntityType()) {
				EntityType et = (EntityType) t.getRef();
				etList.add(et);
			}
			Collections.sort(etList, new Comparator<EntityType>() {
				public int compare(EntityType o1, EntityType o2) {
					return o1.getName().compareTo(o2.getName());
				}
			});
			for (EntityType et : etList) {
				Object obj = new ComboObjectHolder<EntityType>(et);
				view.entityTypeCombo.addItem(obj);
			}
		}		
	}
	
	/**
	 * Sets the languages in the languageCombo to those associated with authority.
	 * 
	 * @param authority
	 */
	private void populateLanguages(Authority authority) {
		view.languageCombo.removeAllItems();
		List<Language> langList = new ArrayList<Language>();
		Authority.Languages authorityLanguages = authority.getLanguages();
		if (authorityLanguages != null) {
			for (Authority.Languages.Language l : authorityLanguages.getLanguage()) {
				Language language = (Language) l.getRef();
				langList.add(language);
			}
			Collections.sort(langList, new Comparator<Language>() {
				public int compare(Language o1, Language o2) {
					return o1.getName().compareTo(o2.getName());
				}
			});
			for (Language l : langList) {
				Object obj = new ComboObjectHolder<Language>(l);
				view.languageCombo.addItem(obj);
				if (l.isUserPreferred() != null && l.isUserPreferred()) {
					view.languageCombo.setSelectedItem(obj);
				}
			}
		}		
	}
	
	/**
	 * Sets the name types in the nameTypeCombo to those associated with authority.
	 * 
	 * @param authority
	 */
	private void populateNameTypes(Authority authority) {
		view.nameTypeCombo.removeAllItems();
		List<NameType> ntList = new ArrayList<NameType>();
		Authority.NameTypes authorityNameTypes = authority.getNameTypes();
		if (authorityNameTypes != null) {
			for (Authority.NameTypes.NameType nt : authorityNameTypes.getNameType()) {
				NameType nameType = (NameType) nt.getRef();
				ntList.add(nameType);
			}
			Collections.sort(ntList, new Comparator<NameType>() {
				public int compare(NameType o1, NameType o2) {
					return o1.getName().compareTo(o2.getName());
				}
			});
			for (NameType nt : ntList) {
				Object obj = new ComboObjectHolder<NameType>(nt);
				view.nameTypeCombo.addItem(obj);
			}
		}
	}

	/**
	 * Sets the scripts in the scriptCombo to those associated with authority.
	 * 
	 * @param authority
	 */
	private void populateScripts(Authority authority) {
		view.scriptCombo.removeAllItems();
		List<Script> scriptList = new ArrayList<Script>();
		Authority.Scripts authorityScripts = authority.getScripts();
		if (authorityScripts != null) {
			for (Authority.Scripts.Script s : authorityScripts.getScript()) {
				Script script = (Script) s.getRef();
				scriptList.add(script);
			}
			Collections.sort(scriptList, new Comparator<Script>() {
				public int compare(Script o1, Script o2) {
					return o1.getName().compareTo(o2.getName());
				}
			});
			for (Script s : scriptList) {
				Object obj = new ComboObjectHolder<Script>(s);
				view.scriptCombo.addItem(obj);
				if (s.isUserPreferred() != null && s.isUserPreferred()) {
					view.scriptCombo.setSelectedItem(obj);
				}
			}
		}
	}
	
	/**
	 * Sets the mouse cursor to the system wait cursor.
	 */
	private void waitCursor() {
		view.setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR));
	}

	/**
	 * Sets the mouse cursor to the system default cursor.
	 */
	private void defaultCursor() {
		view.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
	}

	/**
	 * Displays a dialog window with the exception information
	 * 
	 * @param e
	 *            the exception
	 */
	public void showExceptionDialog(Exception e) {

		JOptionPane.showMessageDialog(view, e.getMessage(), "Exception",
				JOptionPane.ERROR_MESSAGE);

	}

	// ActionListener: JButton actions

	/**
	 * @see java.awt.event.ActionListener#actionPerformed(java.awt.event.ActionEvent)
	 */
	@Override
	public void actionPerformed(ActionEvent e) {

		if (e.getSource().equals(view.preferencesButton)) {
			preferences.showDialog();

			if (preferences.isPreferencesSet()) {
				dispatcher = preferences.getLookupPreferences().getDispatcher();

				closeWindow();

				view.setVisible(false);
				view.dispose();

				view = null;
				view = new LookupView(parent, viewTitle, viewModality);
				table = view.resultsTable;

				initView();

				showView(lookupName, lookupType);
			}
		} else if (e.getSource().equals(view.editButton)) {
			editEntityAction();
		} else if (e.getSource().equals(view.cancelButton)) {
			closeWindow();
		} else if (e.getSource().equals(view.newButton)) {
			try {
				waitCursor();

				setKeyAndType(newAction());

				for (JTextField t : texts) {
					t.setText("");
				}

				closeWindow();
			} catch (DispatcherException ex) {
				showExceptionDialog(ex);
			} finally {
				defaultCursor();
			}
		} else if (e.getSource().equals(view.findButton)) {
			try {
				waitCursor();

				findAction();
			} catch (DispatcherException ex) {
				showExceptionDialog(ex);
			} catch (URISyntaxException ex) {
				showExceptionDialog(ex);
			} finally {
				defaultCursor();
			}

		}

	}

	/**
	 * Closes the window and releases resources.
	 */
	private void closeWindow() {
		view.setVisible(false);
	}

	/**
	 * Opens a link in a browser to edit the selected entity.
	 */
	private void editEntityAction() {

		// gets the selected entity position
		int viewRowIndex = table.getSelectedRow();
		int modelRowIndex = table.convertRowIndexToModel(viewRowIndex);

		// gets the selected entity
		Entity e = (Entity) table.getModel().getValueAt(modelRowIndex,
				ENTITY_COLUMN);

		if (e != null) {
			if (Desktop.isDesktopSupported()) {
				Desktop desktop = Desktop.getDesktop();

				try {
					desktop.browse(new URI(dispatcher.getEditUrl(e)));
				} catch (NullPointerException ex) {
					showExceptionDialog(ex);
				} catch (IOException ex) {
					showExceptionDialog(ex);
				} catch (URISyntaxException ex) {
					showExceptionDialog(ex);
				}
			}
		}

	}

	@SuppressWarnings("unchecked")
	private Entity newAction() throws DispatcherException {

		Collection c = dispatcher.getBaseDocument();

		Entity entity = EatsMlUtils.createEntity(c, "new_entity");

		EatsMlUtils.createExistence(entity, authority);

		EntityType entityType = (EntityType) ((ComboObjectHolder<?>) view.entityTypeCombo
				.getSelectedItem()).getObject();

		EatsMlUtils.createEntityType(entity, authority, entityType);

		NameType nameType = (NameType) ((ComboObjectHolder<?>) view.nameTypeCombo
				.getSelectedItem()).getObject();

		Name nameAssertion = EatsMlUtils.createName(entity,
				authority, nameType, "new_name_assertion", true);

		nameAssertion.setDisplayForm(view.displayNameText.getText());
		nameAssertion
				.setLanguage((Language) ((ComboObjectHolder<Language>) view.languageCombo
						.getSelectedItem()).getObject());
		nameAssertion
				.setScript((Script) ((ComboObjectHolder<Script>) view.scriptCombo
						.getSelectedItem()).getObject());

		if (namePartTypesTextFieldsHash != null) {
			for (NamePartType npt : namePartTypesTextFieldsHash.keySet()) {
				String name = namePartTypesTextFieldsHash.get(npt).getText();
				EatsMlUtils.createNamePart(nameAssertion, npt, name, null, null);
			}
		}

		String url = dispatcher.importDocument(c, "created new entity "
				+ view.displayNameText.getText());

		Collection imported = dispatcher.getProcessedImport(url);

		if (imported == null) {
			throw new DispatcherException(
					"Failed to get the key for the imported entity. The entity has been created, try using search.");
		}

		entity = imported.getEntities().getEntity().get(0);

		return entity;

	}

	private void findAction() throws DispatcherException, URISyntaxException {

		int found = 0;

		clearResults();

		DefaultTableModel model = (DefaultTableModel) table.getModel();

		// executes the search
		searchResults = dispatcher.lookupName(getSearchName());

		Entities entities = searchResults.getEntities();

		if (entities != null) {
			found = ((Entities) searchResults.getEntities()).getEntity().size();
			int namePartTypesCols = 0;
			if (namePartTypesTextFieldsHash != null) {
				namePartTypesCols = namePartTypesTextFieldsHash.size();
			}

			for (Entity entity : entities.getEntity()) {
				Object[] data = new Object[namePartTypesCols + BASE_COLUMN_COUNT];

				data[ENTITY_COLUMN] = entity;

				List<Name> nameList = EatsMlUtils.getDefaultNames(entity);

				if (nameList != null) {
					Name name = nameList.get(0);
					data[ENTITY_DETAILS_COLUMN] = name.getAssembledForm();

					if (name.getNameParts() != null) {
						for (NamePart np : name.getNameParts().getNamePart()) {
							String id = ((NamePartType) np.getNamePartType()).getId();
							int pos = namePartTypesColumnsHash.get(id);
							Script script = (Script) np.getScript();
							if (data[pos] != null) {
								data[pos] = data[pos] + script.getSeparator() + np.getContent();
							} else {
								data[pos] = np.getContent();
							}
						}
					}
				}

				List<EntityType> etList = EatsMlUtils.getAuthorityEntityTypes(entity, authority);

				if (etList != null) {
					data[ENTITY_TYPE_COLUMN] = etList.get(0).getName();
				}

				model.addRow(data);
			}
		}

		view.statusLabel.setText("Found " + found
				+ (found == 1 ? " entity" : " entities"));

	}

	private void clearResults() {

		DefaultTableModel model = (DefaultTableModel) table.getModel();

		// clears the search results table
		while (model.getRowCount() > 0) {
			model.removeRow(0);
		}

		view.detailsTextPane.setText("");

		view.statusLabel.setText(" ");

	}

	/**
	 * Concatenates all the values in the JTextFields.
	 * 
	 * @return String
	 */
	private String getSearchName() {

		StringBuffer buffer = new StringBuffer(view.displayNameText.getText());

		if (texts != null) {
			for (JTextField tf : texts) {
				buffer.append(" ").append(tf.getText());
			}
		}
		
		return buffer.toString().trim();

	}

	// DocumentListener: Handle events from the JTextFields.

	/**
	 * @see javax.swing.event.DocumentListener#changedUpdate(javax.swing.event
	 *      .DocumentEvent)
	 */
	@Override
	public void changedUpdate(DocumentEvent e) {
		// Plain text components do not fire this event
	}

	/**
	 * @see javax.swing.event.DocumentListener#insertUpdate(javax.swing.event.DocumentEvent)
	 */
	@Override
	public void insertUpdate(DocumentEvent e) {
		handleUpdate(e);
	}

	/**
	 * @see javax.swing.event.DocumentListener#removeUpdate(javax.swing.event.DocumentEvent)
	 */
	@Override
	public void removeUpdate(DocumentEvent e) {
		handleUpdate(e);
	}

	private void handleUpdate(DocumentEvent e) {
		if (getSearchName().length() > 0) {
			view.newButton.setEnabled(true);
			view.findButton.setEnabled(true);
		} else {
			view.newButton.setEnabled(false);
			view.findButton.setEnabled(false);
		}
	}

	// ListSelectionListener: to display entity details in a text area.

	/**
	 * @see javax.swing.event.ListSelectionListener#valueChanged(javax.swing.
	 *      event.ListSelectionEvent)
	 */
	@Override
	public void valueChanged(ListSelectionEvent event) {

		JTextPane textPane = view.detailsTextPane;
		int viewRowIndex = table.getSelectedRow();

		if (viewRowIndex < 0) {
			view.editButton.setEnabled(false);

			// selection got filtered away
			textPane.setText("<html />");
		} else {
			view.editButton.setEnabled(true);

			int modelRowIndex = table.convertRowIndexToModel(viewRowIndex);
			Entity entity = (Entity) table.getModel().getValueAt(modelRowIndex,
					ENTITY_COLUMN);

			textPane.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 10));
			textPane.setText("<html />");

			StringBuffer buffer = new StringBuffer();
			buffer.append("<html>");
			buffer.append("<body style='white-space: normal'>");
			buffer.append("<div style='margin: 5px'>");

			List<Date> dateList = EatsMlUtils.getExistencesDates(entity);

			if (dateList != null && dateList.size() > 0) {
				buffer.append("<b>Dates</b>");
				buffer.append("<ul style='list-style-type: none; margin-left: 10px'>");

				for (Date date : dateList) {
					buffer.append("<li>");
					buffer.append(date.getAssembledForm());
					buffer.append("</li>");
				}

				buffer.append("</ul>");
			}
			
			List<Name> defaultNames = EatsMlUtils.getDefaultNames(entity);
			if (defaultNames != null) {
				Name defaultName = defaultNames.get(0);
				List<Name> names = entity.getNames().getName();
				if (names.size() > 1) {
					buffer.append("<b>Other names</b>");
					buffer.append("<ul style='list-style-type: none; margin-left: 10px'>");
					for (Name name : names) {
						if (name != defaultName) {
							buffer.append("<li>");
							buffer.append(name.getAssembledForm());
							buffer.append("</li>");
						}
					}
					buffer.append("</ul>");
				}
				
			}

			List<Note> noteList = EatsMlUtils.getNotes(authority, entity);

			if (noteList != null && noteList.size() > 0) {
				buffer.append("<b>Notes</b>");
				buffer.append("<ul style='list-style-type: none; margin-left: 10px'>");

				for (Note note : noteList) {
					buffer.append("<li><p style='margin-bottom: 5px'>");
					buffer.append(note.getContent());
					buffer.append("</p></li>");
				}

				buffer.append("</ul>");
			}

			EntityRelationships ers = entity.getEntityRelationships();

			if (ers != null) {
				buffer.append("<b>Related Entities</b>");
				buffer.append("<ul style='list-style-type: none; margin-left: 10px'>");

				if (ers != null) {
					for (EntityRelationship er : ers.getEntityRelationship()) {
						String relationship = EatsMlUtils.getRelationshipText(
								searchResults, entity, er);

						if (relationship != null) {
							buffer.append("<li>");
							buffer.append(relationship);
							buffer.append("</li>");
						}
					}
				}

				buffer.append("</ul>");
			}

			buffer.append("</div>");
			buffer.append("</body>");
			buffer.append("</html>");

			textPane.setText(buffer.toString());
			textPane.setCaretPosition(0);
		}
	}

	// HyperlinkListener

	/**
	 * This method opens the browser and browses to the URL in the JEditorPane.
	 */
	@Override
	public void hyperlinkUpdate(HyperlinkEvent e) {

		if (e.getEventType() == HyperlinkEvent.EventType.ACTIVATED) {
			if (Desktop.isDesktopSupported()) {
				Desktop desktop = Desktop.getDesktop();

				try {
					desktop.browse(new URI(e.getURL().toString()));
				} catch (NullPointerException ex) {
					showExceptionDialog(ex);
				} catch (IOException ex) {
					showExceptionDialog(ex);
				} catch (URISyntaxException ex) {
					showExceptionDialog(ex);
				}
			}
		}
	}

	//

	/**
	 * Sets the key and type using the current selected entity.
	 * 
	 * @param e
	 *            the entity. If null uses the current selected entity
	 */
	private void setKeyAndType(Entity entity) {

		if (entity == null) {
			int viewRowIndex = table.getSelectedRow();

			if (viewRowIndex >= 0) {
				int modelRowIndex = table.convertRowIndexToModel(viewRowIndex);

				entity = (Entity) table.getModel().getValueAt(modelRowIndex,
						ENTITY_COLUMN);

				type = (String) table.getModel().getValueAt(modelRowIndex,
						ENTITY_TYPE_COLUMN);
			}

		} else {
			type = ((EntityType) entity.getEntityTypes()
					.getEntityType().get(0).getEntityType())
					.getName();
		}

		key = entity.getUrl();

	}

	/**
	 * Displays the pre-populated lookup form.
	 * 
	 * @param name
	 *            the name to look up
	 * @param type
	 *            the entity type
	 */
	public void showView(String name, String type) {

		lookupName = name;
		lookupType = type;

		view.displayNameText.setText(name);

		if (type != null && type.length() > 0) {
			for (int idx = 0; idx < view.entityTypeCombo.getItemCount(); idx++) {
				if (type.equals(view.entityTypeCombo.getItemAt(idx).toString())) {
					view.entityTypeCombo.setSelectedIndex(idx);
					break;
				}
			}
		}

		key = null;
		type = null;

		clearResults();

		view.setVisible(true);

	}

	// private classes

	/**
	 * Holder class that wraps objects that are stored in the combo boxes.
	 */
	private class ComboObjectHolder<T> {

		private Object obj = null;

		/**
		 * @param obj
		 */
		public ComboObjectHolder(Object obj) {
			this.obj = obj;
		}

		public String toString() {

			if (obj instanceof EntityType) {
				return ((EntityType) obj).getName();
			} else if (obj instanceof Language) {
				return ((Language) obj).getName();
			} else if (obj instanceof Script) {
				return ((Script) obj).getName();
			} else if (obj instanceof NameType) {
				return ((NameType) obj).getName();
			}

			return null;

		}

		public Object getObject() {
			return obj;
		}
	}

	// Getters & Setters

	/**
	 * @return the dispatcher
	 */
	public Dispatcher getDispatcher() {
		return dispatcher;
	}

	/**
	 * @param dispatcher
	 *            the dispatcher to set
	 */
	public void setDispatcher(Dispatcher dispatcher) {
		this.dispatcher = dispatcher;
	}

	/**
	 * @return the key
	 */
	public String getKey() {
		return key;
	}

	/**
	 * @return the searchResults
	 */
	public Collection getSearchResults() {
		return searchResults;
	}

	/**
	 * @param searchResults
	 *            the searchResults to set
	 */
	public void setSearchResults(Collection searchResults) {
		this.searchResults = searchResults;
	}

	/**
	 * @return the type
	 */
	public String getType() {
		return type;
	}

	/**
	 * @return the view
	 */
	public LookupView getView() {
		return view;
	}

}
