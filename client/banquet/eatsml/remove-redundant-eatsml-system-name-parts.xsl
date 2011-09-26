<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:e="http://hdl.handle.net/10063/234"
                version="1.0">

  <!-- Remove redundant system name part types. -->

  <xsl:template match="e:system_name_part_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:system_name_part_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="../e:name_part_types/e:name_part_type/@system_name_part_type=current()/e:system_name_part_type/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="../e:languages/e:language/e:system_name_part_types/e:system_name_part_type/@ref=current()/e:system_name_part_type/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text>false</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <xsl:if test="$keep='true'">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:system_name_part_type[@eats_id]">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="../../e:name_part_types/e:name_part_type/@system_name_part_type=current()/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="../../e:languages/e:language/e:system_name_part_types/e:system_name_part_type/@ref=current()/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text>false</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <xsl:if test="$keep='true'">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>