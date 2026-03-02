// Import the rendercv function and all the refactored components
#import "@preview/rendercv:0.1.0": *

// Apply the rendercv template with custom configuration
#show: rendercv.with(
  name: "Ben Walzer",
  footer: context { [#emph[Ben Walzer -- #str(here().page())\/#str(counter(page).final().first())]] },
  top-note: [ #emph[Last updated in Mar 2026] ],
  locale-catalog-language: "en",
  page-size: "us-letter",
  page-top-margin: 0.7in,
  page-bottom-margin: 0.7in,
  page-left-margin: 0.7in,
  page-right-margin: 0.7in,
  page-show-footer: true,
  page-show-top-note: true,
  colors-body: rgb(0, 0, 0),
  colors-name: rgb(0, 79, 144),
  colors-headline: rgb(0, 79, 144),
  colors-connections: rgb(0, 79, 144),
  colors-section-titles: rgb(0, 79, 144),
  colors-links: rgb(0, 79, 144),
  colors-footer: rgb(128, 128, 128),
  colors-top-note: rgb(128, 128, 128),
  typography-line-spacing: 0.6em,
  typography-alignment: "justified",
  typography-date-and-location-column-alignment: right,
  typography-font-family-body: "Source Sans 3",
  typography-font-family-name: "Source Sans 3",
  typography-font-family-headline: "Source Sans 3",
  typography-font-family-connections: "Source Sans 3",
  typography-font-family-section-titles: "Source Sans 3",
  typography-font-size-body: 10pt,
  typography-font-size-name: 30pt,
  typography-font-size-headline: 10pt,
  typography-font-size-connections: 10pt,
  typography-font-size-section-titles: 1.4em,
  typography-small-caps-name: false,
  typography-small-caps-headline: false,
  typography-small-caps-connections: false,
  typography-small-caps-section-titles: false,
  typography-bold-name: true,
  typography-bold-headline: false,
  typography-bold-connections: false,
  typography-bold-section-titles: true,
  links-underline: false,
  links-show-external-link-icon: false,
  header-alignment: center,
  header-photo-width: 3.5cm,
  header-space-below-name: 0.7cm,
  header-space-below-headline: 0.7cm,
  header-space-below-connections: 0.7cm,
  header-connections-hyperlink: true,
  header-connections-show-icons: true,
  header-connections-display-urls-instead-of-usernames: false,
  header-connections-separator: "",
  header-connections-space-between-connections: 0.5cm,
  section-titles-type: "with_partial_line",
  section-titles-line-thickness: 0.5pt,
  section-titles-space-above: 0.5cm,
  section-titles-space-below: 0.3cm,
  sections-allow-page-break: true,
  sections-space-between-text-based-entries: 0.3em,
  sections-space-between-regular-entries: 1.2em,
  entries-date-and-location-width: 4.15cm,
  entries-side-space: 0.2cm,
  entries-space-between-columns: 0.1cm,
  entries-allow-page-break: false,
  entries-short-second-row: true,
  entries-summary-space-left: 0cm,
  entries-summary-space-above: 0cm,
  entries-highlights-bullet:  "•" ,
  entries-highlights-nested-bullet:  "•" ,
  entries-highlights-space-left: 0.15cm,
  entries-highlights-space-above: 0cm,
  entries-highlights-space-between-items: 0cm,
  entries-highlights-space-between-bullet-and-text: 0.5em,
  date: datetime(
    year: 2026,
    month: 3,
    day: 2,
  ),
)


= Ben Walzer

#connections(
  [#connection-with-icon("location-dot")[Falls Church, VA]],
  [#link("mailto:benjamin.walzer4@gmail.com", icon: false, if-underline: false, if-color: false)[#connection-with-icon("envelope")[benjamin.walzer4\@gmail.com]]],
  [#link("tel:+1-757-374-1691", icon: false, if-underline: false, if-color: false)[#connection-with-icon("phone")[(757) 374-1691]]],
)


== Summary

Strategic analytics leader adept at dissecting ambiguous business challenges, leveraging full data science lifecycle expertise to deliver actionable insights and compelling recommendations. Proven track record of architecting robust data solutions, from core BI to advanced causal modeling, and driving their implementation to achieve quantifiable strategic impact.

== Experience

#regular-entry(
  [
    #strong[Kalman & Company, Inc.], Senior Consultant, Data Analytics

    - Directed a cross-functional team of 10 engineers and analysts to architect end-to-end analytical frameworks, transforming raw mission data into prescriptive intelligence for executive leadership.

    - Engineered a readiness platform for 17K+ global assets; leveraged SQL-based methodology and interactive visualization to conduct spatiotemporal root-cause analysis on downtime trends, resulting in an accelerated, proactive diagnostic framework that reduced time to discovery by over 10 days.

    - Modernized enterprise-scale financial forecasting by architecting automated Databricks ETL pipelines; consolidated disparate, legacy transactional streams into a unified Data Lakehouse, achieving a 12\% increase in forecasting accuracy through the deployment of advanced time-series ensemble models.

    - Developed a scalable Python automation framework to modernize complex inventory audit workflows; eliminated manual data disparities and reduced reporting latency by 80\%, ensuring the high-fidelity data integrity required to secure consecutive unmodified audit opinions for the USMC.

  ],
  [
    Arlington, VA

    July 2024 – present

    1 year 9 months

  ],
)

#regular-entry(
  [
    #strong[Kalman & Company, Inc.], Consultant, Data Analytics

    - Directed an enterprise-wide Business Intelligence suite for 500+ stakeholders, centralizing disparate financial streams into a unified Power BI ecosystem; automated 60\% of manual reporting tasks, reducing report generation time from hours to seconds and accelerating the fiscal decision-making cycle.

    - Spearheaded data architecture for a Coast Guard Data Warehouse and automated Python\/SQL ETL pipelines to unify disparate silos into a single source of truth; engineered predictive maintenance models and self-service BI suites that transitioned leadership from reactive reporting to proactive, data-driven asset management.

  ],
  [
    Arlington, VA

    Aug 2020 – present

    5 years 8 months

  ],
)

== Skills

#strong[Data Engineering & Cloud Platforms:] ETL, Data Engineering, Databricks, Spark, BigQuery, Azure

#strong[Business Intelligence & Visualization:] Power BI, Tableau, Excel, Power Query, Power Automate, Power Apps
