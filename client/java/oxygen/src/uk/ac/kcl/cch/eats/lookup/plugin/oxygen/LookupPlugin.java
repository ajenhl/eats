/**
 * LookupPlugin.java
 * Sep 28, 2010
 */
package uk.ac.kcl.cch.eats.lookup.plugin.oxygen;

import java.awt.Frame;

import ro.sync.exml.plugin.Plugin;
import ro.sync.exml.plugin.PluginDescriptor;
import uk.ac.kcl.cch.eats.dispatcher.DispatcherException;
import uk.ac.kcl.cch.eats.lookup.LookupController;
import uk.ac.kcl.cch.eats.lookup.LookupPreferencesController;

/**
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 * 
 */
public class LookupPlugin extends Plugin {

    /**
     * Plugin instance.
     */
    private static LookupPlugin instance = null;

    /**
     * Keeps only one instance of the lookup controller.
     */
    private static LookupController lookupController = null;

    /**
     * Creates a new LookupPlugin.
     * 
     * @param descriptor
     *            plugin descriptor object
     */
    public LookupPlugin(PluginDescriptor descriptor) {
        super(descriptor);

        if (instance != null) {
            throw new IllegalStateException("Already instantiated !");
        }

        instance = this;
    }

    public static LookupPlugin getInstance() {
        return instance;
    }

    /**
     * @return the lookupController
     * @throws DispatcherException
     */
    public static LookupController getLookupController(Frame frame,
            LookupPreferencesController preferences) throws DispatcherException {

        if (lookupController == null) {
            lookupController = new LookupController(preferences, frame, "Look up name", true);
        }

        return lookupController;

    }

    /**
     * @param lookupController
     *            the lookupController to set
     */
    public static void setLookupController(LookupController lookupController) {
        LookupPlugin.lookupController = lookupController;
    }

}
