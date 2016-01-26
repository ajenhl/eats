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
import javax.xml.bind.annotation.XmlIDREF;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;


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
 *         &lt;element name="name" maxOccurs="unbounded">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                 &lt;sequence>
 *                   &lt;element ref="{http://eats.artefact.org.nz/ns/eatsml/}assembled_form" minOccurs="0"/>
 *                   &lt;element ref="{http://eats.artefact.org.nz/ns/eatsml/}display_form"/>
 *                   &lt;element ref="{http://eats.artefact.org.nz/ns/eatsml/}name_parts" minOccurs="0"/>
 *                   &lt;group ref="{http://eats.artefact.org.nz/ns/eatsml/}dates"/>
 *                   &lt;group ref="{http://eats.artefact.org.nz/ns/eatsml/}non_assertion_notes"/>
 *                 &lt;/sequence>
 *                 &lt;attGroup ref="{http://eats.artefact.org.nz/ns/eatsml/}authority_attribute"/>
 *                 &lt;attGroup ref="{http://eats.artefact.org.nz/ns/eatsml/}is_preferred_attribute"/>
 *                 &lt;attGroup ref="{http://eats.artefact.org.nz/ns/eatsml/}script_attribute"/>
 *                 &lt;attGroup ref="{http://eats.artefact.org.nz/ns/eatsml/}language_attribute"/>
 *                 &lt;attribute name="eats_id" type="{http://www.w3.org/2001/XMLSchema}anySimpleType" />
 *                 &lt;attribute name="name_type" use="required" type="{http://www.w3.org/2001/XMLSchema}IDREF" />
 *                 &lt;attribute name="user_preferred" type="{http://www.w3.org/2001/XMLSchema}boolean" />
 *               &lt;/restriction>
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
    "name"
})
@XmlRootElement(name = "names")
public class Names {

    @XmlElement(required = true)
    protected List<Names.Name> name;

    /**
     * Gets the value of the name property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the name property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getName().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Names.Name }
     * 
     * 
     */
    public List<Names.Name> getName() {
        if (name == null) {
            this.name = new ArrayList<Names.Name>();
        }
        return name;
    }


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
     *         &lt;element ref="{http://eats.artefact.org.nz/ns/eatsml/}assembled_form" minOccurs="0"/>
     *         &lt;element ref="{http://eats.artefact.org.nz/ns/eatsml/}display_form"/>
     *         &lt;element ref="{http://eats.artefact.org.nz/ns/eatsml/}name_parts" minOccurs="0"/>
     *         &lt;group ref="{http://eats.artefact.org.nz/ns/eatsml/}dates"/>
     *         &lt;group ref="{http://eats.artefact.org.nz/ns/eatsml/}non_assertion_notes"/>
     *       &lt;/sequence>
     *       &lt;attGroup ref="{http://eats.artefact.org.nz/ns/eatsml/}authority_attribute"/>
     *       &lt;attGroup ref="{http://eats.artefact.org.nz/ns/eatsml/}is_preferred_attribute"/>
     *       &lt;attGroup ref="{http://eats.artefact.org.nz/ns/eatsml/}script_attribute"/>
     *       &lt;attGroup ref="{http://eats.artefact.org.nz/ns/eatsml/}language_attribute"/>
     *       &lt;attribute name="eats_id" type="{http://www.w3.org/2001/XMLSchema}anySimpleType" />
     *       &lt;attribute name="name_type" use="required" type="{http://www.w3.org/2001/XMLSchema}IDREF" />
     *       &lt;attribute name="user_preferred" type="{http://www.w3.org/2001/XMLSchema}boolean" />
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "assembledForm",
        "displayForm",
        "nameParts",
        "dates",
        "notes"
    })
    public static class Name {

        @XmlElement(name = "assembled_form")
        protected String assembledForm;
        @XmlElement(name = "display_form", required = true)
        protected String displayForm;
        @XmlElement(name = "name_parts")
        protected NameParts nameParts;
        protected Dates dates;
        protected nz.org.artefact.eats.ns.eatsml.Date.Notes notes;
        @XmlAttribute(name = "eats_id")
        @XmlSchemaType(name = "anySimpleType")
        protected String eatsId;
        @XmlAttribute(name = "name_type", required = true)
        @XmlIDREF
        @XmlSchemaType(name = "IDREF")
        protected Object nameType;
        @XmlAttribute(name = "user_preferred")
        protected Boolean userPreferred;
        @XmlAttribute(name = "authority", required = true)
        @XmlIDREF
        @XmlSchemaType(name = "IDREF")
        protected Object authority;
        @XmlAttribute(name = "is_preferred", required = true)
        protected boolean isPreferred;
        @XmlAttribute(name = "script", required = true)
        @XmlIDREF
        @XmlSchemaType(name = "IDREF")
        protected Object script;
        @XmlAttribute(name = "language", required = true)
        @XmlIDREF
        @XmlSchemaType(name = "IDREF")
        protected Object language;

        /**
         * Gets the value of the assembledForm property.
         * 
         * @return
         *     possible object is
         *     {@link String }
         *     
         */
        public String getAssembledForm() {
            return assembledForm;
        }

        /**
         * Sets the value of the assembledForm property.
         * 
         * @param value
         *     allowed object is
         *     {@link String }
         *     
         */
        public void setAssembledForm(String value) {
            this.assembledForm = value;
        }

        /**
         * Gets the value of the displayForm property.
         * 
         * @return
         *     possible object is
         *     {@link String }
         *     
         */
        public String getDisplayForm() {
            return displayForm;
        }

        /**
         * Sets the value of the displayForm property.
         * 
         * @param value
         *     allowed object is
         *     {@link String }
         *     
         */
        public void setDisplayForm(String value) {
            this.displayForm = value;
        }

        /**
         * Gets the value of the nameParts property.
         * 
         * @return
         *     possible object is
         *     {@link NameParts }
         *     
         */
        public NameParts getNameParts() {
            return nameParts;
        }

        /**
         * Sets the value of the nameParts property.
         * 
         * @param value
         *     allowed object is
         *     {@link NameParts }
         *     
         */
        public void setNameParts(NameParts value) {
            this.nameParts = value;
        }

        /**
         * Gets the value of the dates property.
         * 
         * @return
         *     possible object is
         *     {@link Dates }
         *     
         */
        public Dates getDates() {
            return dates;
        }

        /**
         * Sets the value of the dates property.
         * 
         * @param value
         *     allowed object is
         *     {@link Dates }
         *     
         */
        public void setDates(Dates value) {
            this.dates = value;
        }

        /**
         * Gets the value of the notes property.
         * 
         * @return
         *     possible object is
         *     {@link nz.org.artefact.eats.ns.eatsml.Date.Notes }
         *     
         */
        public nz.org.artefact.eats.ns.eatsml.Date.Notes getNotes() {
            return notes;
        }

        /**
         * Sets the value of the notes property.
         * 
         * @param value
         *     allowed object is
         *     {@link nz.org.artefact.eats.ns.eatsml.Date.Notes }
         *     
         */
        public void setNotes(nz.org.artefact.eats.ns.eatsml.Date.Notes value) {
            this.notes = value;
        }

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
         * Gets the value of the nameType property.
         * 
         * @return
         *     possible object is
         *     {@link Object }
         *     
         */
        public Object getNameType() {
            return nameType;
        }

        /**
         * Sets the value of the nameType property.
         * 
         * @param value
         *     allowed object is
         *     {@link Object }
         *     
         */
        public void setNameType(Object value) {
            this.nameType = value;
        }

        /**
         * Gets the value of the userPreferred property.
         * 
         * @return
         *     possible object is
         *     {@link Boolean }
         *     
         */
        public Boolean isUserPreferred() {
        	if (userPreferred == null) {
        		userPreferred = false;
        	}
            return userPreferred;
        }

        /**
         * Sets the value of the userPreferred property.
         * 
         * @param value
         *     allowed object is
         *     {@link Boolean }
         *     
         */
        public void setUserPreferred(Boolean value) {
            this.userPreferred = value;
        }

        /**
         * Gets the value of the authority property.
         * 
         * @return
         *     possible object is
         *     {@link Object }
         *     
         */
        public Object getAuthority() {
            return authority;
        }

        /**
         * Sets the value of the authority property.
         * 
         * @param value
         *     allowed object is
         *     {@link Object }
         *     
         */
        public void setAuthority(Object value) {
            this.authority = value;
        }

        /**
         * Gets the value of the isPreferred property.
         * 
         */
        public boolean isIsPreferred() {
            return isPreferred;
        }

        /**
         * Sets the value of the isPreferred property.
         * 
         */
        public void setIsPreferred(boolean value) {
            this.isPreferred = value;
        }

        /**
         * Gets the value of the script property.
         * 
         * @return
         *     possible object is
         *     {@link Object }
         *     
         */
        public Object getScript() {
            return script;
        }

        /**
         * Sets the value of the script property.
         * 
         * @param value
         *     allowed object is
         *     {@link Object }
         *     
         */
        public void setScript(Object value) {
            this.script = value;
        }

        /**
         * Gets the value of the language property.
         * 
         * @return
         *     possible object is
         *     {@link Object }
         *     
         */
        public Object getLanguage() {
            return language;
        }

        /**
         * Sets the value of the language property.
         * 
         * @param value
         *     allowed object is
         *     {@link Object }
         *     
         */
        public void setLanguage(Object value) {
            this.language = value;
        }

    }

}