package nz.ac.victoria.wtapress.eats.lookup.plugin.jedit;

import java.util.Hashtable;

import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

public class SaxDefaultHandler extends DefaultHandler {

    private Hashtable<String, String> nsHash = new Hashtable<String, String>();
    
    /**
     * Collects all the namespaces in the current XML document.
     * 
     * @see org.xml.sax.helpers.DefaultHandler#startPrefixMapping(java.lang.String,
     *      java.lang.String)
     */
    @Override
    public void startPrefixMapping(String prefix, String uri) throws SAXException {
		nsHash.put(uri, prefix);
    }
    
    public Hashtable<String, String> getNsHash() {
    	return nsHash;
    }

}
