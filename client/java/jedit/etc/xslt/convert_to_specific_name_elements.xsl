<xsl:stylesheet version="1.0" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- Convert generic TEI name elements that are annotated with an
       @orig_element into specific elements.
       
       This XSLT should not be customised. Configuration of the
       mapping between TEI elements and the TEI name element is all
       handled in convert_from_specific_name_elements.xsl. -->

  <xsl:output omit-xml-declaration="yes" />

  <xsl:template match="tei:name[@orig_element]">
    <xsl:element name="tei:{@orig_element}">
      <xsl:apply-templates select="@*|node()" />
    </xsl:element>
  </xsl:template>

  <xsl:template match="@orig_element" />

  <xsl:template match="@added_type" />

  <xsl:template match="tei:name[@added_type]/@type" />

  <xsl:template match="tei:name[not(@orig_element)][@type]">
    <xsl:variable name="element-name">
      <xsl:choose>
        <xsl:when test="@type = 'person'">persName</xsl:when>
        <xsl:when test="@type = 'place'">placeName</xsl:when>
        <xsl:when test="@type = 'organisation'">orgName</xsl:when>
        <xsl:when test="@type = 'organization'">orgName</xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="local-name()" />
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <xsl:element name="{$element-name}" namespace="http://www.tei-c.org/ns/1.0">
      <xsl:apply-templates select="@*[not(name() = 'type')]" />

      <xsl:if test="$element-name = local-name()">
        <xsl:copy-of select="@type" />
      </xsl:if>
      
      <xsl:apply-templates />
    </xsl:element>
  </xsl:template>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()" />
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
