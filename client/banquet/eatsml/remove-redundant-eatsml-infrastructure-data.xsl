<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:e="http://eats.artefact.org.nz/ns/eatsml/" version="1.0">

  <!-- Remove redundant infrastructural material from an EATSML import
       file. -->

  <xsl:output indent="yes"/>
  <xsl:strip-space elements="*"/>
  <xsl:preserve-space elements="e:separator"/>

  <!-- Remove authorities that are not used in a property
       assertion. -->
  <xsl:template match="e:authority[@eats_id]">
    <xsl:if test="/e:collection/e:entities/e:entity/*/*[@authority=current()/@xml:id]">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused calendars from authority. -->
  <xsl:template match="e:authority/e:calendars">
    <xsl:if test="e:collection/e:entities/e:entity/*/*[@authority=current()/../@xml:id]/e:dates/e:date/e:date_parts/e:date_part/@calendar=current()/e:calendar/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:authority/e:calendars/e:calendar">
    <xsl:if test="e:collection/e:entities/e:entity/*/*[@authority=current()/../../@xml:id]/e:dates/e:date/e:date_parts/e:date_part/@calendar=current()/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused date periods from authority. -->
  <xsl:template match="e:authority/e:date_periods">
    <xsl:if test="/e:collection/e:entities/e:entity/*/*[@authority=current()/../@xml:id]/e:dates/e:date/@date_period=current()/e:date_period/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:authority/e:date_periods/e:date_period">
    <xsl:if test="/e:collection/e:entities/e:entity/*/*[@authority=current()/../../@xml:id]/e:dates/e:date/@date_period=current()/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused date types from authority. -->
  <xsl:template match="e:authority/e:date_types">
    <xsl:if test="/e:collection/e:entities/e:entity/*/*[@authority=current()/../@xml_id]/e:dates/e:date/e:date_parts/e:date_part/@date_type=current()/e:date_type/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:authority/e:date_types/e:date_type">
    <xsl:if test="/e:collection/e:entities/e:entity/*/*[@authority=current()/../../@xml_id]/e:dates/e:date/e:date_parts/e:date_part/@date_type=current()/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused entity relationship types from authority. -->
  <xsl:template match="e:authority/e:entity_relationship_types">
    <xsl:if test="/e:collection/e:entities/e:entity/e:entity_relationships/e:entity_relationship[@authority=current()/../@xml_id]/@entity_relationship_type=current()/e:entity_relationship_type/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:authority/e:entity_relationship_types/e:entity_relationship_types">
    <xsl:if test="/e:collection/e:entities/e:entity/e:entity_relationships/e:entity_relationship[@authority=current()/../../@xml_id]/@entity_relationship_type=current()/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused entity types from authority. -->
  <xsl:template match="e:authority/e:entity_types">
    <xsl:if test="/e:collection/e:entities/e:entity/e:entity_types/e:entity_type[@authority=current()/../@xml:id]/@entity_type=current()/e:entity_type/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:authority/e:entity_types/e:entity_type">
    <xsl:if test="/e:collection/e:entities/e:entity/e:entity_types/e:entity_type[@authority=current()/../../@xml:id]/@entity_type=current()/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused languages from authority. -->
  <xsl:template match="e:authority/e:languages">
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../@xml:id]/@language=current()/e:language/@ref or
                  /e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../@xml:id]/e:name_parts/e:name_part/@language=current()/e:language/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:authority/e:languages/e:language">
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../../@xml:id]/@language=current()/@ref or
                  /e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../../@xml:id]/e:name_parts/e:name_part/@language=current()/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused name part types from authority. -->
  <xsl:template match="e:authority/e:name_part_types">
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../@xml:id]/e:name_parts/e:name_part/@name_part_type=current()/e:name_part_type/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:authority/e:name_part_types/e:name_part_type">
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../../@xml:id]/e:name_parts/e:name_part/@name_part_type=current()/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused name types from authority. -->
  <xsl:template match="e:authority/e:name_types">
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../@xml:id]/@name_type=current()/e:name_type/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:authority/e:name_types/e:name_type">
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../../@xml:id]/@name_type=current()/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused scripts from authority. -->
  <xsl:template match="e:authority/e:scripts">
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../@xml:id]/@script=current()/e:script/@ref or
                  /e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../@xml:id]/e:name_parts/e:name_part/@script=current()/e:script/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:authority/e:scripts">
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../../@xml:id]/@script=current()/@ref or
                  /e:collection/e:entities/e:entity/e:names/e:name[@authority=current()/../../@xml:id]/e:name_parts/e:name_part/@script=current()/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused calendars. -->
  <xsl:template match="e:collection/e:calendars">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:calendar[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_parts/e:date_part/@calendar=current()/e:calendar/@xml:id">
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
    <xsl:if test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_parts/e:date_part/@calendar=current()/@xml:id">
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
        <xsl:when test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/@date_period=current()/e:date_period/@xml:id">
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
    <xsl:if test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/@date_period=current()/@xml:id">
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
        <xsl:when test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_parts/e:date_part/@date_type=current()/e:date_type/@xml:id">
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
    <xsl:if test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_parts/e:date_part/@date_type=current()/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused entity relationship types. -->
  <xsl:template match="e:entity_relationship_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:entity_relationship_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:entity_relationships/e:entity_relationship/@entity_relationship_type=current()/e:entity_relationship_type/@xml:id">
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
    <xsl:if test="/e:collection/e:entities/e:entity/e:entity_relationships/e:entity_relationship/@entity_relationship_type=current()/@xml:id">
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
    <xsl:if test="/e:collection/e:entities/e:entity/e:entity_types/e:entity_type/@entity_type=current()/@xml:id">
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
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name/@language=current()/@xml:id or
                  /e:collection/e:entities/e:entity/e:names/e:name/e:name_parts/e:name_part/@language=current()/e:language/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unusued name part types from language. -->
  <xsl:template match="e:language/e:name_part_types">
    <xsl:if test="e:collection/e:entities/e:entity/e:names/e:name/e:name_parts/e:name_part[@language=current()/../@xml:id]/@name_part_type=current()/e:name_part_type/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>
  <xsl:template match="e:language/e:name_part_types/e:name_part_type">
    <xsl:if test="e:collection/e:entities/e:entity/e:names/e:name/e:name_parts/e:name_part[@language=current()/../../@xml:id]/@name_part_type=current()/@ref">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
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
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name/e:name_parts/e:name_part/@name_part_type=current()/@xml:id">
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
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name/@name_type=current()/@xml:id">
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
    <xsl:if test="/e:collection/e:entities/e:entity/e:names/e:name/@script=current()/@xml:id or
                  /e:collection/e:entities/e:entity/e:names/e:name/e:name_parts/e:name_part/@script=current()/e:script/@xml:id">
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