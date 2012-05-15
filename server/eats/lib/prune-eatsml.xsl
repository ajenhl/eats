<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:e="http://eats.artefact.org.nz/ns/eatsml/" version="1.0">

  <!-- Remove redundant infrastructural material from an EATSML import
       file.
       
       An element that does not have an @eats_id is retained, since it
       is new. An element that has an @eats_id is retained if it is
       referenced by a property assertion, a new authority, or a new
       language.
       
       References within an existing authority or language are
       removed.

  -->

  <xsl:output indent="yes"/>
  <xsl:strip-space elements="*"/>
  <xsl:preserve-space elements="e:separator"/>

  <!-- Remove authorities that are not used in a property
       assertion. -->
  <xsl:template match="e:authorities">
    <xsl:if test="e:authority[not(@eats_id)] or /e:collection/e:entities/e:entity/*/*[@authority=current()/e:authority/@xml:id]">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:authority[@eats_id]">
    <xsl:if test="/e:collection/e:entities/e:entity/*/*[@authority=current()/@xml:id]">
      <xsl:copy>
        <xsl:apply-templates select="@*|e:name"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:authority[not(@eats_id)]">
    <xsl:copy-of select="." />
  </xsl:template>

  <!-- Remove unused calendars. -->
  <xsl:template match="e:collection/e:calendars">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:calendar[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_parts/e:date_part[@calendar]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:authorities/e:authority[not(@eats_id)]/e:calendars/e:calendar">
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
  <xsl:template match="e:collection/e:calendars/e:calendar[@eats_id]">
    <xsl:variable name="xml_id" select="@xml:id" />
    <xsl:if test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_parts/e:date_part/@calendar=$xml_id or
                  /e:collection/e:authorities/e:authority[not(@eats_id)]/e:calendars/e:calendar/@ref=$xml_id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused date periods. -->
  <xsl:template match="e:collection/e:date_periods">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:date_period[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date[@date_period]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:authorities/e:authority[not(@eats_id)]/e:date_periods/e:date_period">
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
  <xsl:template match="e:collection/e:date_periods/e:date_period[@eats_id]">
    <xsl:variable name="xml_id" select="@xml:id" />
    <xsl:if test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/@date_period=$xml_id or
                  /e:collection/e:authorities/e:authority[not(@eats_id)]/e:date_periods/e:date_period/@ref=$xml_id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused date types. -->
  <xsl:template match="e:collection/e:date_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:date_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_parts/e:date_part[@date_type]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:authorities/e:authority[not(@eats_id)]/e:date_types/e:date_type">
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
  <xsl:template match="e:collection/e:date_types/e:date_type[@eats_id]">
    <xsl:variable name="xml_id" select="@xml:id" />
    <xsl:if test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_parts/e:date_part/@date_type=$xml_id or
                  /e:collection/e:authorities/e:authority[not(@eats_id)]/e:date_types/e:date_type/@ref=$xml_id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused entity relationship types. -->
  <xsl:template match="e:collection/e:entity_relationship_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:entity_relationship_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:entity_relationships/e:entity_relationship/@entity_relationship_type=current()/e:entity_relationship_type/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:authorities/e:authority[not(@eats_id)]/e:entity_relationship_types/e:entity_relationship_type">
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
  <xsl:template match="e:collection/e:entity_relationship_types/e:entity_relationship_type[@eats_id]">
    <xsl:variable name="xml_id" select="@xml:id" />
    <xsl:if test="/e:collection/e:entities/e:entity/e:entity_relationships/e:entity_relationship/@entity_relationship_type=$xml_id or
                  /e:collection/e:authorities/e:authority[not(@eats_id)]/e:entity_relationship_types/e:entity_relationship_type/@ref=$xml_id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused entity types. -->
  <xsl:template match="e:collection/e:entity_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:entity_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:entity_types/e:entity_type/@entity_type=current()/e:entity_type/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:authorities/e:authority[not(@eats_id)]/e:entity_types/e:entity_type">
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
  <xsl:template match="e:collection/e:entity_types/e:entity_type[@eats_id]">
    <xsl:variable name="xml_id" select="@xml:id" />
    <xsl:if test="/e:collection/e:entities/e:entity/e:entity_types/e:entity_type/@entity_type=$xml_id or
                  /e:collection/e:authorities/e:authority[not(@eats_id)]/e:entity_types/e:entity_type/@ref=$xml_id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused languages. -->
  <xsl:template match="e:collection/e:languages">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:language[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:names/e:name/@language=current()/e:language/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:names/e:name/e:name_parts/e:name_part/@language=current()/e:language/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:authorities/e:authority[not(@eats_id)]/e:languages/e:language">
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
  <xsl:template match="e:collection/e:languages/e:language[@eats_id]">
    <xsl:variable name="xml_id" select="@xml:id" />
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name/@language=$xml_id or
                  /e:collection/e:entities/e:entity/e:names/e:name/e:name_parts/e:name_part/@language=$xml_id or
                  /e:collection/e:authorities/e:authority[not(@eats_id)]/e:languages/e:language/@ref=$xml_id">
      <xsl:copy>
        <xsl:apply-templates select="@*|e:name|e:code"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused name part types. -->
  <xsl:template match="e:collection/e:name_part_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:name_part_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:names/e:name/e:name_parts/e:name_part/@name_part_type=current()/e:name_part_type/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:authorities/e:authority[not(@eats_id)]/e:name_part_types/e:name_part_type">
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
  <xsl:template match="e:collection/e:name_part_types/e:name_part_type[@eats_id]">
    <xsl:variable name="xml_id" select="@xml:id" />
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name/e:name_parts/e:name_part/@name_part_type=$xml_id or
                  /e:collection/e:authorities/e:authority[not(@eats_id)]/e:name_part_types/e:name_part_type/@ref=$xml_id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused name types. -->
  <xsl:template match="e:collection/e:name_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:name_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:names/e:name/@name_type=current()/e:name_type/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:authorities/e:authority[not(@eats_id)]/e:name_types/e:name_type">
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
  <xsl:template match="e:collection/e:name_types/e:name_type[@eats_id]">
    <xsl:variable name="xml_id" select="@xml:id" />
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name/@name_type=$xml_id or
                  /e:collection/e:authorities/e:authority[not(@eats_id)]/e:name_types/e:name_type/@ref=$xml_id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused scripts. -->
  <xsl:template match="e:collection/e:scripts">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:script[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:names/e:name/@script=current()/e:script/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:names/e:name/e:name_parts/e:name_part/@script=current()/e:script/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:authorities/e:authority[not(@eats_id)]/e:scripts/e:script">
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
  <xsl:template match="e:script[@eats_id]">
    <xsl:variable name="xml_id" select="@xml:id" />
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name/@script=$xml_id or
                  /e:collection/e:entities/e:entity/e:names/e:name/e:name_parts/e:name_part/@script=$xml_id or
                  /e:collection/e:authorities/e:authority[not(@eats_id)]/e:scripts/e:script/@ref=$xml_id">
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