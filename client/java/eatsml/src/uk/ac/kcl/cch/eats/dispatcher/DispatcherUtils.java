/**
 * DispatcherUtils.java
 * Sep 8, 2010
 */
package uk.ac.kcl.cch.eats.dispatcher;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.UnsupportedEncodingException;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;

import nz.org.artefact.eats.ns.eatsml.Collection;

/**
 * Utility class for the @see Dispather class.
 * 
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 */
public class DispatcherUtils {

    /**
     * Unmarshalls the content of an EATS response and creates the corresponding
     * object. For more information see {@link https
     * ://jaxb.dev.java.net/tutorial
     * /section_3_1-Unmarshalling-and-Using-the-Data.html#Unmarshalling}
     * 
     * @param xml
     *            the contents to unmarshall
     * 
     * @return Collection
     * @throws JAXBException
     * @throws UnsupportedEncodingException
     */
    public static Collection unmarshal(String xml) throws JAXBException,
            UnsupportedEncodingException {

        JAXBContext jc = JAXBContext.newInstance(Collection.class);

        Unmarshaller u = jc.createUnmarshaller();

        return (Collection) u.unmarshal(new ByteArrayInputStream(xml
                .getBytes(Dispatcher.DEFAULT_ENCODING)));

    }

    /**
     * Serializes the collection object into EATSML.
     * 
     * @param c
     *            the collection to serialize
     * @return EATSML String
     * @throws JAXBException
     * @throws UnsupportedEncodingException
     */
    public static String marshall(Collection c) throws JAXBException, UnsupportedEncodingException {

        JAXBContext jc = JAXBContext.newInstance(Collection.class);

        ByteArrayOutputStream eatsml = new ByteArrayOutputStream();

        jc.createMarshaller().marshal(c, eatsml);

        return eatsml.toString(Dispatcher.DEFAULT_ENCODING);

    }

    /**
     * Transforms an XML String using the given stylesheet.
     * 
     * @param input
     *            the XML String to be transformed
     * @param transformer
     *            XSLT transformer
     * @return XML String
     * @throws DispatcherException
     */
    public static String transform(String input, Transformer transformer)
            throws DispatcherException {

        try {
            ByteArrayOutputStream output = new ByteArrayOutputStream();

            // transforms the source XML to the output file
            transformer.transform(new StreamSource(new ByteArrayInputStream(input.getBytes())),
                    new StreamResult(output));

            return output.toString(Dispatcher.DEFAULT_ENCODING);
        } catch (TransformerConfigurationException e) {
            throw new DispatcherException(e.getMessage());
        } catch (TransformerFactoryConfigurationError e) {
            throw new DispatcherException(e.getMessage());
        } catch (TransformerException e) {
            throw new DispatcherException(e.getMessage());
        } catch (UnsupportedEncodingException e) {
            throw new DispatcherException(e.getMessage());
        }

    }

}
