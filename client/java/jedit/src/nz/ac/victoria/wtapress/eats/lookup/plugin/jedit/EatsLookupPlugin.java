package nz.ac.victoria.wtapress.eats.lookup.plugin.jedit;

import java.io.ByteArrayInputStream;
import java.util.Hashtable;

import javax.swing.JOptionPane;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.gjt.sp.jedit.EditPlugin;
import org.gjt.sp.jedit.View;
import org.gjt.sp.jedit.buffer.JEditBuffer;
import org.gjt.sp.jedit.textarea.JEditTextArea;
import org.gjt.sp.jedit.textarea.Selection;
import uk.ac.kcl.cch.eats.dispatcher.DispatcherException;
import uk.ac.kcl.cch.eats.lookup.LookupController;
import uk.ac.kcl.cch.eats.lookup.LookupPreferencesController;
import uk.ac.kcl.cch.eats.lookup.TEIName;

public class EatsLookupPlugin extends EditPlugin {

	public static final String NAME = "eatslookup";

    /**
     * Keeps only one instance of the lookup controller.
     */
    private static LookupController lookupController = null;

    public void lookup (View view, String entityType) {
        JEditTextArea textArea = view.getTextArea();
        JEditBuffer buffer = textArea.getBuffer();
        int count = textArea.getSelectionCount();
        if (count == 1) {
            Selection selection = textArea.getSelection(0);
            String name = textArea.getSelectedText(selection);
            if (name != null) {
                String result = lookupName(view, buffer, name);
                textArea.setBuffer(buffer);
                textArea.setSelectedText(selection, result);
            }
        }
    }
    
    private String lookupName (View view, JEditBuffer buffer, String name) {
    	String result = name;
    	String xsltPath = getPluginHome().getPath(); 
        LookupPreferencesController lookupPreferencesController = LookupPreferencesController.getInstance(view);

        try {
        	SAXParserFactory factory = SAXParserFactory.newInstance();
        	factory.setNamespaceAware(true);
        	SAXParser parser = factory.newSAXParser();
        	SaxDefaultHandler handler = new SaxDefaultHandler();
        	int textLength = buffer.getLength();
        	ByteArrayInputStream inputStream = new ByteArrayInputStream(buffer.getText(0, textLength).getBytes()); 
        	parser.parse(inputStream, handler);

        	if (!lookupPreferencesController.isPreferencesSet()) {
        		lookupPreferencesController.showDialog();

        		if (!lookupPreferencesController.isPreferencesSet()) {
        			return null;
        		}
        	}

        	Hashtable<String, String> nsHash = handler.getNsHash();
        	TEIName teiName = new TEIName(name, nsHash, xsltPath);

        	LookupController lookupController = getLookupController(view, lookupPreferencesController);
        	lookupController.showView(teiName.getNameString(), "person");
        	String key = lookupController.getKey();

        	if (key != null && key.length() > 0) {
        		teiName.setKey(key);

        		String type = lookupController.getType();

        		if (type != null && type.length() > 0) {
        			teiName.setType(type);
        		}

        		result = teiName.getXmlName();
        	}

        } catch (Exception e) {
        	lookupPreferencesController.setPreferencesSet(false);
        	e.printStackTrace();

        	JOptionPane.showMessageDialog(view, e.getMessage(), "Exception",
        			JOptionPane.ERROR_MESSAGE);
        }
    	return result;
    }
    
    /**
     * @return the lookupController
     * @throws DispatcherException
     */
    public static LookupController getLookupController(View view,
            LookupPreferencesController preferences) throws DispatcherException {

        if (lookupController == null) {
            lookupController = new LookupController(preferences, view, "Look up name", true);
        }

        return lookupController;

    }

}