<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:template match="name">
    <xsl:variable name="normalized-text" select="normalize-space(.)"/>
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:choose>
        <xsl:when test="$normalized-text">
          <xsl:if test="substring(., 1, 1) != substring($normalized-text, 1, 1)">
            <xsl:text> </xsl:text>
          </xsl:if>
          <xsl:value-of select="$normalized-text"/>
          <xsl:if test="substring(., string-length(.), 1) != substring($normalized-text, string-length($normalized-text), 1)">
            <xsl:text> </xsl:text>
          </xsl:if>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text>[name element has no textual content]</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="preceding">
    <xsl:variable name="text">
      <xsl:for-each select="chunk">
        <xsl:sort select="position()" data-type="number" order="descending"/>
        <xsl:value-of select="."/>
      </xsl:for-each>
    </xsl:variable>
    <xsl:variable name="normalized-text" select="normalize-space($text)"/>
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:if test="$normalized-text">
        <xsl:value-of select="$normalized-text"/>
        <xsl:if test="substring($text, string-length($text), 1) != substring($normalized-text, string-length($normalized-text), 1)">
          <xsl:text> </xsl:text>
        </xsl:if>
      </xsl:if>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="following">
    <xsl:variable name="normalized-text" select="normalize-space(.)"/>
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:if test="$normalized-text">
        <xsl:if test="substring(., 1, 1) != substring($normalized-text, 1, 1)">
          <xsl:text> </xsl:text>
        </xsl:if>
        <xsl:value-of select="$normalized-text"/>
      </xsl:if>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>