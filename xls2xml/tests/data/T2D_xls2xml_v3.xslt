<?xml version="1.0"?>
<!--
This XML file defines mapping rules for converting an Excel worksheet or TSV file to an XML document

Conceptually speaking, the Excel worksheet or TSV file is parsed first into an intermediate XML
document that contains field names as tags and field values as texts. This intermediate XML document
is then transformed into final XML document through XSLT transformation.

You could define multiple templates here, each catering for different schema.

Please note that because XML tag must start with a letter or underscore and contains only
letters, digits, hyphens, underscores and periods, any violating characters should be replaced
with underscores.
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
                xmlns:regexp="http://exslt.org/regular-expressions"
                extension-element-prefixes="regexp">
<xsl:output method="xml" indent="yes"/>
<xsl:template match="SampleSet"><!-->Should match <key_in_config>+'Set'<-->
  <SAMPLE_SET noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.sample.xsd">
    <xsl:for-each select="Sample"><!-->Should select from <key_in_config><-->
      <SAMPLE>
        <xsl:attribute name="center_name">
            <xsl:value-of select="Center_name"/>
        </xsl:attribute>
        <DESCRIPTION><xsl:value-of select="Description"/></DESCRIPTION>
        <SAMPLE_NAME>
            <TAXON_ID>9606</TAXON_ID>
            <SCIENTIFIC_NAME>homo sapiens</SCIENTIFIC_NAME>
            <COMMON_NAME>human</COMMON_NAME>
        </SAMPLE_NAME>
        <SAMPLE_ATTRIBUTES>
            <SAMPLE_ATTRIBUTE>
                <TAG>subject_id</TAG>
                <VALUE><xsl:value-of select="Subject_ID"/></VALUE>
            </SAMPLE_ATTRIBUTE>
            <SAMPLE_ATTRIBUTE>
                <TAG>sample_id</TAG>
                <VALUE><xsl:value-of select="Sample_ID"/></VALUE>
            </SAMPLE_ATTRIBUTE>
            <SAMPLE_ATTRIBUTE>
                <TAG>cell_type</TAG>
                <VALUE><xsl:value-of select="Cell_Type"/></VALUE>
            </SAMPLE_ATTRIBUTE>
            <SAMPLE_ATTRIBUTE>
                <TAG>gender</TAG>
                <VALUE><xsl:value-of select="Gender"/></VALUE>
            </SAMPLE_ATTRIBUTE>
            <SAMPLE_ATTRIBUTE>
                <TAG>T2D</TAG>
                <VALUE><xsl:value-of select="T2D"/></VALUE>
            </SAMPLE_ATTRIBUTE>
            <SAMPLE_ATTRIBUTE>
                <TAG>year_of_birth</TAG>
                <VALUE><xsl:value-of select="Year_of_Birth"/></VALUE>
            </SAMPLE_ATTRIBUTE>
            <xsl:for-each select="*">
              <xsl:if test="regexp:test(name(.), '^attribute__[a-z0-9_]*_$')">
                <SAMPLE_ATTRIBUTE>
                  <TAG><xsl:value-of select="name(.)"/></TAG>
                  <VALUE><xsl:value-of select="."/></VALUE>
                </SAMPLE_ATTRIBUTE>
              </xsl:if>
            </xsl:for-each>
        </SAMPLE_ATTRIBUTES>
      </SAMPLE>
    </xsl:for-each>
  </SAMPLE_SET>
</xsl:template>

<xsl:template match="AnalysisSet">
  <ANALYSIS_SET noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.analysis.xsd">
    <xsl:for-each select="Analysis">
      <ANALYSIS>
        <xsl:attribute name="analysis_center">
            <xsl:value-of select="Center_name"/>
        </xsl:attribute>
        <xsl:attribute name="analysis_date">
            <xsl:value-of select="Analysis_date"/>
        </xsl:attribute>
        <TITLE><xsl:value-of select="Title"/></TITLE>
        <DESCRIPTION><xsl:value-of select="Description"/></DESCRIPTION>
        <EXPERIMENT_REF><xsl:value-of select="Experiment_type"/></EXPERIMENT_REF>
        <RUN_REF><xsl:value-of select="Run_Accession_s_"/></RUN_REF>
        <ANALYSIS_LINKS><xsl:value-of select="External_link"/></ANALYSIS_LINKS>
      </ANALYSIS>
    </xsl:for-each>
  </ANALYSIS_SET>
</xsl:template>

</xsl:stylesheet>
