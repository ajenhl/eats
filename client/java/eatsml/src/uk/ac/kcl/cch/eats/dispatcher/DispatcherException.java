/**
 * EatsException.java
 * Sep 3, 2010
 */
package uk.ac.kcl.cch.eats.dispatcher;

/**
 * Exception class for EATS related exceptions.
 * 
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 */
public class DispatcherException extends Exception {

    private static final long serialVersionUID = 8914884291519428144L;

    /**
     * Creates a new DispatcherException.
     * 
     * @param message
     */
    public DispatcherException(String message) {
        super(message);
    }

    /**
     * Creates a new DispatcherException.
     * 
     * @param message
     */
    public DispatcherException(String message, Exception e) {
        super(message, e);
    }

}
