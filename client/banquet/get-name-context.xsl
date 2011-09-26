<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0"
                version="1.0">

  <xsl:param name="context_length" select="80"/>

  <xsl:template match="/">
    <key_instances>
      <xsl:apply-templates select="//tei:name | //tei:rs"/>
    </key_instances>
  </xsl:template>

  <xsl:template match="tei:name | tei:rs">
    <key_instance>
      <name>
        <xsl:apply-templates select=".//text()"/>
      </name>
      <preceding>
        <xsl:apply-templates select="preceding::text()[1]" mode="preceding"/>
      </preceding>
      <following>
        <xsl:apply-templates select="following::text()[1]" mode="following"/>
      </following>
    </key_instance>
  </xsl:template>

  <xsl:template match="text()" mode="preceding">
    <xsl:param name="length-needed" select="$context_length"/>
    <xsl:variable name="text">
      <xsl:call-template name="normalize-space">
        <xsl:with-param name="text" select="."/>
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="text-length" select="string-length($text)"/>
    <chunk>
      <xsl:choose>
        <xsl:when test="$text-length &lt; $length-needed">
          <xsl:value-of select="$text"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="substring($text, $text-length - $length-needed + 1, $length-needed)"/>
        </xsl:otherwise>
      </xsl:choose>
    </chunk>
    <xsl:if test="$text-length &lt; $length-needed">
      <xsl:apply-templates select="preceding::text()[1]" mode="preceding">
        <xsl:with-param name="length-needed" select="$length-needed - $text-length"/>
      </xsl:apply-templates>
    </xsl:if>
  </xsl:template>

  <xsl:template match="text()" mode="following">
    <xsl:param name="length-needed" select="$context_length"/>
    <xsl:variable name="text">
      <xsl:call-template name="normalize-space">
        <xsl:with-param name="text" select="."/>
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="text-length" select="string-length($text)"/>
    <xsl:choose>
      <xsl:when test="$text-length &lt; $length-needed">
        <xsl:value-of select="$text"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="substring($text, 1, $length-needed)"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="$text-length &lt; $length-needed">
      <xsl:apply-templates select="following::text()[1]" mode="following">
        <xsl:with-param name="length-needed" select="$length-needed - $text-length"/>
      </xsl:apply-templates>
    </xsl:if>
  </xsl:template>

  <!-- Text nodes that are not to be used. -->
  <xsl:template match="text()[ancestor::tei:choice][not(ancestor::tei:orig or ancestor::tei:abbr or ancestor::tei:sic)]"/>

  <xsl:template match="text()[ancestor::tei:choice][not(ancestor::tei:orig or ancestor::tei:abbr or ancestor::tei:sic)]" mode="preceding">
    <xsl:param name="length-needed" select="$context_length"/>
    <xsl:apply-templates select="preceding::text()[1]" mode="preceding">
      <xsl:with-param name="length-needed" select="$length-needed"/>
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="text()[ancestor::tei:choice][not(ancestor::tei:orig or ancestor::tei:abbr or ancestor::tei:sic)]" mode="following">
    <xsl:param name="length-needed" select="$context_length"/>
    <xsl:apply-templates select="following::text()[1]" mode="following">
      <xsl:with-param name="length-needed" select="$length-needed"/>
    </xsl:apply-templates>
  </xsl:template>

  <!-- Return a string with sequences of whitespace characters
       replaced by a single space, but retaining leading and trailing
       whitespace. -->
  <xsl:template name="normalize-space">
    <xsl:param name="text"/>
    <xsl:variable name="normalized-text" select="normalize-space($text)"/>
    <xsl:variable name="first-char" select="substring($text, 1, 1)"/>
    <xsl:variable name="first-normalized-char"
                  select="substring($normalized-text, 1, 1)"/>
    <xsl:variable name="final-char"
                  select="substring($text, string-length($text), 1)"/>
    <xsl:variable name="final-normalized-char"
                  select="substring($normalized-text, string-length($normalized-text), 1)"/>
    <xsl:if test="$first-char != $first-normalized-char">
      <xsl:text> </xsl:text>
    </xsl:if>
    <xsl:value-of select="$normalized-text"/>
    <xsl:if test="$normalized-text and $final-char != $final-normalized-char">
      <xsl:text> </xsl:text>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>