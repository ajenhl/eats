<xsl:stylesheet version="1.0"
                xmlns:tei="http://www.tei-c.org/ns/1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- Convert specific name elements in a TEI document to name
       elements with an @type.
       
       This XSLT may be customised by adding/removing/changing
       template matches for TEI elements, calling the template
       make-name to convert them into TEI name elements with a
       particular type.
       
       Such conversion does not clobber any existing type attribute,
       which remains and is used by Banquet as an indicator of the
       entity type. -->
  <xsl:output omit-xml-declaration="yes"/>

  <xsl:template match="tei:geogName">
    <xsl:call-template name="make-name">
      <xsl:with-param name="type" select="'geographic'"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tei:orgName">
    <xsl:call-template name="make-name">
      <xsl:with-param name="type" select="'organisation'"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tei:persName">
    <xsl:call-template name="make-name">
      <xsl:with-param name="type" select="'person'"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tei:placeName">
    <xsl:call-template name="make-name">
      <xsl:with-param name="type" select="'place'"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="make-name">
    <xsl:param name="type"/>
    <tei:name orig_element="{local-name()}">
      <xsl:if test="not(@type)">
        <xsl:attribute name="type">
          <xsl:value-of select="$type"/>
        </xsl:attribute>
        <xsl:attribute name="added_type">
          <xsl:text>true</xsl:text>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates select="@*|node()"/>
    </tei:name>
  </xsl:template>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>