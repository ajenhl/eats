<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:e="http://hdl.handle.net/10063/234" version="1.0">

  <!-- Remove redundant infrastructural material from an EATSML import
       file. This is done as a separate step from the entity data
       removal, since the criteria for removing infrastructural
       material is whether it is linked from the entity data. -->

  <xsl:output indent="yes"/>
  <xsl:strip-space elements="*"/>

  <!-- Remove authorities that are not used in an authority
       record. Other infrastructural elements reference authorities,
       but we can ignore checking them since it's ultimately the
       entity information that is important. -->
  <xsl:template match="e:authority[@eats_id]">
    <xsl:if test="/e:collection/e:authority_records/e:authority_record/@authority=current()/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unwanted authority attributes. -->
  <xsl:template match="@default_calendar"/>
  <xsl:template match="@default_date_period"/>
  <xsl:template match="@default_date_type"/>
  <xsl:template match="@default_language"/>
  <xsl:template match="@default_script"/>

  <!-- Remove unused entity types. -->
  <xsl:template match="e:entity_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:entity_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:entity_type_assertions/e:entity_type_assertion/@entity_type=current()/e:entity_type/@xml:id">
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
  <xsl:template match="e:entity_type[@eats_id]">
    <xsl:if test="/e:collection/e:entities/e:entity/e:entity_type_assertions/e:entity_type_assertion/@entity_type=current()/@xml:id">
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
        <xsl:when test="/e:collection/e:entities/e:entity/e:entity_relationship_assertions/e:entity_relationship_assertion/@type=current()/e:entity_relationship_type/@xml:id">
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
  <xsl:template match="e:entity_relationship_type[@eats_id]">
    <xsl:if test="/e:collection/e:entities/e:entity/e:entity_relationship_assertions/e:entity_relationship_assertion/@type=current()/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused name types. -->
  <xsl:template match="e:name_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:name_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/@type=current()/e:name_type/@xml:id">
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
  <xsl:template match="e:name_type[@eats_id]">
    <xsl:if test="/e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/@type=current()/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused name part types. -->
  <xsl:template match="e:name_part_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:name_part_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/e:name_parts/e:name_part/@type=current()/e:name_part_type/@xml:id">
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
  <xsl:template match="e:name_part_type[@eats_id]">
    <xsl:if test="/e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/e:name_parts/e:name_part/@type=current()/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused languages. -->
  <xsl:template match="e:languages">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:language[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/@language=current()/e:language/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/e:name_parts/e:name_part/@language=current()/e:language/@xml:id">
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
  <xsl:template match="e:language[@eats_id]">
    <xsl:if test="/e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/@language=current()/@xml:id or
                  /e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/e:name_parts/e:name_part/@language=current()/e:language/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused scripts. -->
  <xsl:template match="e:scripts">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:script[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/@script=current()/e:script/@xml:id">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/e:name_parts/e:name_part/@script=current()/e:script/@xml:id">
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
    <xsl:if test="/e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/@script=current()/@xml:id or
                  /e:collection/e:entities/e:entity/e:name_assertions/e:name_assertion/e:name_parts/e:name_part/@script=current()/e:script/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused name relationship types. -->
  <xsl:template match="e:name_relationship_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:name_relationship_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/e:name_relationship_assertions/e:name_relationship_assertion/@type=current()/e:name_relationship_type/@xml:id">
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
  <xsl:template match="e:name_relationship_type[@eats_id]">
    <xsl:if test="/e:collection/e:entities/e:entity/e:name_relationship_assertions/e:name_relationship_assertion/@type=current()/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused date periods. -->
  <xsl:template match="e:date_periods">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:date_period[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/@period=current()/e:date_period/@xml:id">
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
  <xsl:template match="e:date_period[@eats_id]">
    <xsl:if test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/@period=current()/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused date types. -->
  <xsl:template match="e:date_types">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:date_type[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_part/@date_type=current()/e:date_type/@xml:id">
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
  <xsl:template match="e:date_type[@eats_id]">
    <xsl:if test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_part/@date_type=current()/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove unused calendars. -->
  <xsl:template match="e:calendars">
    <xsl:variable name="keep">
      <xsl:choose>
        <xsl:when test="e:calendar[not(@eats_id)]">
          <xsl:text>true</xsl:text>
        </xsl:when>
        <xsl:when test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_part/@calendar=current()/e:calendar/@xml:id">
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
  <xsl:template match="e:calendar[@eats_id]">
    <xsl:if test="/e:collection/e:entities/e:entity/*/*/e:dates/e:date/e:date_part/@calendar=current()/@xml:id">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <xsl:template match="e:authority_record">
    <xsl:if test="/e:collection/e:entities/e:entity/*/*/@authority_record=current()/@xml:id">
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