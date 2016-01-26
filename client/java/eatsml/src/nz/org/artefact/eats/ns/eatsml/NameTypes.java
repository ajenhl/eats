//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.8-b130911.1802 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2015.12.11 at 10:13:18 AM NZDT 
//


package nz.org.artefact.eats.ns.eatsml;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlID;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.CollapsedStringAdapter;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;


/**
 * <p>Java class for anonymous complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="name_type" maxOccurs="unbounded">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;extension base="{http://eats.artefact.org.nz/ns/eatsml/}name">
 *                 &lt;attGroup ref="{http://eats.artefact.org.nz/ns/eatsml/}id_attribute"/>
 *                 &lt;attribute name="eats_id" type="{http://www.w3.org/2001/XMLSchema}anySimpleType" />
 *               &lt;/extension>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "nameType"
})
@XmlRootElement(name = "name_types")
public class NameTypes {

    @XmlElement(name = "name_type", required = true)
    protected List<NameTypes.NameType> nameType;

    /**
     * Gets the value of the nameType property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the nameType property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getNameType().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link NameTypes.NameType }
     * 
     * 
     */
    public List<NameTypes.NameType> getNameType() {
        if (nameType == null) {
            nameType = new ArrayList<NameTypes.NameType>();
        }
        return this.nameType;
    }


    /**
     * <p>Java class for anonymous complex type.
     * 
     * <p>The following schema fragment specifies the expected content contained within this class.
     * 
     * <pre>
     * &lt;complexType>
     *   &lt;complexContent>
     *     &lt;extension base="{http://eats.artefact.org.nz/ns/eatsml/}name">
     *       &lt;attGroup ref="{http://eats.artefact.org.nz/ns/eatsml/}id_attribute"/>
     *       &lt;attribute name="eats_id" type="{http://www.w3.org/2001/XMLSchema}anySimpleType" />
     *     &lt;/extension>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "")
    public static class NameType
        extends Name
    {

        @XmlAttribute(name = "eats_id")
        @XmlSchemaType(name = "anySimpleType")
        protected String eatsId;
        @XmlAttribute(name = "id", namespace = "http://www.w3.org/XML/1998/namespace", required = true)
        @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
        @XmlID
        @XmlSchemaType(name = "ID")
        protected String id;

        /**
         * Gets the value of the eatsId property.
         * 
         * @return
         *     possible object is
         *     {@link String }
         *     
         */
        public String getEatsId() {
            return eatsId;
        }

        /**
         * Sets the value of the eatsId property.
         * 
         * @param value
         *     allowed object is
         *     {@link String }
         *     
         */
        public void setEatsId(String value) {
            this.eatsId = value;
        }

        /**
         * Gets the value of the id property.
         * 
         * @return
         *     possible object is
         *     {@link String }
         *     
         */
        public String getId() {
            return id;
        }

        /**
         * Sets the value of the id property.
         * 
         * @param value
         *     allowed object is
         *     {@link String }
         *     
         */
        public void setId(String value) {
            this.id = value;
        }

    }

}