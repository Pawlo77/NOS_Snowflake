---
pandoc_args: ["--toc", "--toc-depth=2"]
geometry: "left=2cm,right=2cm,top=3cm,bottom=3cm"
export_on_save:
    pandoc: true
output:
    pdf_document:
        toc: true
        number_sections: true
links-as-notes: true
linkcolor: blue
documentclass: article
papersize: a4
hyperrefoptions:
- linktoc=all
link-citations: true
header-includes:
    - \usepackage{amsmath}

title: Network Operating System
subtitle: Developing market-worthy models using cloud developement
abstract: \
    In this project, we explore the integration of machine learning into Snowflake’s cloud-native ecosystem to create a scalable, efficient, and user-friendly solution. Leveraging Snowpark for model development and deployment, and Snowsight for interactive evaluation, the project bridges technical innovation with practical usability. By embedding ML workflows directly into Snowflake, we eliminate the complexity of external infrastructure while ensuring seamless scalability and robust security. The solution also includes an intuitive graphical user interface (GUI) tailored for both end-users and data scientists, enabling effortless interaction with the model and comprehensive performance analysis. This approach demonstrates the power of modern cloud platforms to simplify and optimize ML workflows for diverse stakeholders.
author:
- Paweł Pozorski, Zuzanna Sieńko
date: "2024-12-23"
lang: en-EN
---

\newpage{}

# Introdution

In an era where data is one of the most valuable assets, organizations strive to leverage machine learning (ML) to gain actionable insights and drive innovation. However, integrating ML into existing workflows often poses challenges, including high infrastructure costs, complex deployment pipelines, and the need for scalable, user-friendly solutions. This project aims to address these challenges by combining the power of Snowflake’s Snowpark and Snowsight platforms to deliver an end-to-end ML solution.  

The primary goal of this project is to develop, deploy, and evaluate a machine learning model using Snowpark, Snowflake’s advanced framework for executing ML and data processing tasks directly within the Snowflake ecosystem. By capitalizing on Snowflake’s inherent advantages, such as cloud-native scalability, secure architecture, and seamless integration with existing data pipelines, this project eliminates the overhead of managing external infrastructure.  

To ensure accessibility and usability, the solution includes a user-friendly graphical user interface (GUI) designed for two key stakeholders: end-users and data scientists. The GUI will allow end-users to interact with the deployed model effortlessly, accessing its predictions and insights in a clear and intuitive manner. For data scientists, the interface, powered by Snowsight, will provide robust tools to evaluate and refine the model’s performance, ensuring continuous optimization.  

From a technical perspective, this project highlights the efficiency of embedding ML workflows directly within Snowflake. It explores the use of Snowpark to preprocess data, train the model, and implement inference capabilities, all while utilizing Snowflake’s secure, high-performance computing environment. Furthermore, the project demonstrates how Snowsight can enhance the model evaluation process, providing interactive dashboards and visualizations that foster collaboration and decision-making.  

By merging cutting-edge technology with practical usability, this project not only meets the requirements of the network operating system labs but also exemplifies how modern cloud platforms can simplify and enhance the development, deployment, and adoption of machine learning solutions.  