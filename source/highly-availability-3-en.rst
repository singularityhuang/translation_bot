.. _architectures:

=======================================================================================
High Availability Architecture and Maximum High Availability Features
=======================================================================================

Get acquainted with the high availability features used in MAA solutions to make architecture-based adjustments. Below is a graphical and textual overview of the main high availability architectures.

- `Introduction to High Availability Architectures <#architectures>`_
- `Introduction to Maximum High Availability <#architectures>`_


Introduction to High Availability Architecture
---------------------------------------------------------

KingbaseES Read-Write Separation Cluster Architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Read-Write Separation Cluster High Availability Architecture

Key Features:

a: Multi-instance redundancy that supports instance-level (including remote) disaster recovery switching.  
    
b: Independent node storage with multiple data redundancies, supporting data (storage) level disaster recovery, where any intact storage within the cluster can restore other node media failures.

c: Balances application read-write load by directing transactional systems to the primary database and read-only systems to the standby database, achieving read-write separation and balanced load.

d: Supports bad block detection and repair.


KingbaseES Clusterware Shared Storage Cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Clusterware Shared Storage Cluster High Availability Architecture

Key Features:

a: Unified management of global resources.

b: Supports high availability and active-active configurations with shared storage.

c: Distributes the application load across different database instances.

d: Decentralized design that provides high throughput, high pressure tolerance, and high load capacity for the cluster system.


Kingbase FlySync Heterogeneous Data Synchronization Architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Kingbase FlySync Heterogeneous Data Synchronization High Availability Architecture

Key Features:

a: Supports zero-downtime version upgrades for homogeneous databases.  
    
b: Enables synchronization across heterogeneous databases and supports remote disaster recovery.

c: Facilitates smooth transitions for domestic database replacements, enabling heterogeneous data synchronization, dual-track operation, and secure switching.


Comparison of High Availability Architectures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

• Choosing Between Read-Write Separation Cluster and Clusterware

.. table:: Comparison of Read-Write Separation Cluster and Clusterware
    :widths: 2 5 5 
    :class: longtable

    +--------------------+----------------------------------+---------------------------------+
    | Comparison Item    | Read-Write Separation Cluster    | Clusterware                     |
    +====================+==================================+=================================+
    | Unplanned Failure  | Offers broader capabilities,     | Relies on storage devices' high |
    | Handling           | handling site failures, storage  | availability architecture for   |
    | Capability         | failures, and device-related     | handling storage and data       |
    |                    | issues, detailed in Chapter 5.   | corruption, detailed in         |
    |                    |                                  | Chapter 5.                      |
    +--------------------+----------------------------------+---------------------------------+
    | Planned            | Supports more comprehensive      | Detailed in Chapter 6.          |
    | Maintenance        | migration-type maintenance       |                                 |
    | Handling           | through physical replication,    |                                 |
    | Capability         | detailed in Chapter 6.           |                                 |
    +--------------------+----------------------------------+---------------------------------+
    | RPO                | Synchronous mode supports        | Supports zero loss.             |
    |                    | zero loss.                       |                                 |
    +--------------------+----------------------------------+---------------------------------+
    | RTO                | Seconds to minutes, with         | Seconds to minutes, with        |
    |                    | automatic fault detection and    | automatic fault detection and   |
    |                    | switching.                       | switching.                      |
    +--------------------+----------------------------------+---------------------------------+
    | Network Location   | No network restrictions within   | Cluster nodes need to be within |
    |                    | the cluster, limited only by     | the same subnet.                |
    |                    | latency due to distance.         |                                 |
    +--------------------+----------------------------------+---------------------------------+
    | Runtime Overhead   | Synchronous mode slightly        | No additional overhead.         |
    |                    | increases transaction commit     |                                 |
    |                    | latency; log transmission        |                                 |
    |                    | consumes minimal CPU and         |                                 |
    |                    | network bandwidth.               |                                 |
    +--------------------+----------------------------------+---------------------------------+
    | Scalability        | Standby supports read operations | Supports running different      |
    |                    | and read-write separation.       | database instances on multiple  |
    |                    |                                  | nodes, supporting load          |
    |                    |                                  | balancing across databases.     |
    +--------------------+----------------------------------+---------------------------------+
    | Equipment Cost     | Relatively low, with a higher    | Relatively high, requires shared|
    |                    | demand for storage capacity,     | storage devices, smaller        |
    |                    | but without the need for         | database layer storage capacity |
    |                    | dedicated storage devices or     | demand, but often requires      |
    |                    | storage networks.                | redundant storage devices to    |
    |                    |                                  | ensure storage reliability.     |
    +--------------------+----------------------------------+---------------------------------+
    
• Choosing Between Read-Write Separation Cluster and Heterogeneous Data Synchronization Software

.. table:: Comparison of Read-Write Separation Cluster and Heterogeneous Data Synchronization Software
    :widths: 2 5 5 
    :class: longtable

    +--------------------+-----------------------+-----------------------+
    | Comparison Item    | Read-Write Separation | Heterogeneous Data    |
    |                    | Cluster               | Synchronization       |
    +====================+=======================+=======================+
    | Unplanned Failure  | Detailed in Chapter 5.| Supports high         |
    | Handling Capability|                       | availability          |
    |                    |                       | architecture using    |
    |                    |                       | heterogeneous database|
    |                    |                       | replication, such as  |
    |                    |                       | dual-track operation  |
    |                    |                       | during replacement.   |
    +--------------------+-----------------------+-----------------------+
    | Planned Maintenance| More suitable for     | Can be implemented    |
    | Handling Capability| migration tasks that  | through project       |
    |                    | require physical      | services for physical |
    |                    | compatibility and for | incompatibility       |
    |                    | system upgrades.      | migration and         |
    |                    |                       | application upgrades. |
    +--------------------+-----------------------+-----------------------+
    | RPO                | Synchronous mode      | Near zero loss.       |
    |                    | supports zero loss.   |                       |
    +--------------------+-----------------------+-----------------------+
    | RTO                | Seconds to minutes,   | Seconds to minutes,   |
    |                    | with automatic fault  | more disaster recovery|
    |                    | detection and         | scenarios use         |
    |                    | switching.            | custom switching.     |
    +--------------------+-----------------------+-----------------------+
    | Supported Topology | One primary, multiple | Can achieve multiple  |
    |                    | standbys, cascading.  | primaries.            |
    +--------------------+-----------------------+-----------------------+
    | Disaster Recovery  | Simple maintenance,   | Supports partial      |
    | Advantage          | data consistency      | database backup,      |
    |                    | without bad blocks.   | reducing bandwidth    |
    |                    |                       | overhead and latency. |
    +--------------------+-----------------------+-----------------------+

Introduction to Maximum High Availability Features
------------------------------------------------------------------------------

• Kingbase Data Watch Cluster Software (Kingbase Data Watch): 
  An integrated high-reliability data solution that prevents data loss or database service interruptions caused by hardware and software failures, natural disasters, or human errors, providing 24/7 uninterrupted database service to meet data security and high availability requirements.

• KingbaseES Read-Write Separation Cluster (KingbaseRWC): 
  The KingbaseES Read-Write Separation Cluster ensures high availability, data protection, and disaster recovery for enterprise data through physical replication, while also providing load balancing for read requests.

.. seealso:: 

   For more information about KingbaseRWC Cluster, please refer to "Best Practices for High Availability in KingbaseES".

• KingbaseES Clusterware: 
  The supporting component of KingbaseES shared storage clusters. It enhances the high availability of multi-node read-write clusters.

.. seealso:: 

   For more information about KingbaseES Clusterware cluster configuration, please refer to "KingbaseES Clusterware Configuration Manual".
 
• Kingbase Heterogeneous Data Synchronization Software (Kingbase FlySync): 
  Kingbase FlySync supports real-time data synchronization across heterogeneous platforms and databases.
  
.. seealso:: 

   For more information about Kingbase FlySync, please refer to the official manual at: "`Kingbase FlySync Product Manual <https://help.kingbase.com.cn/kfs/index.html>`_".

• KingbaseES Backup and Recovery Management Tool (sys_rman): 
  The KingbaseES backup and recovery management tool provides reliable and convenient backup and recovery operations.

.. seealso:: 

   For more information about the backup and recovery management tool, please refer to "KingbaseES Backup and Recovery Tool Manual".
 
• KingbaseES Data Corruption Detection: 
  Detects database bad blocks through checksum technology, including real-time monitoring during operation and detection of backup data.

.. seealso:: 

   For more information about data corruption detection and automatic repair, please refer to `sys_checksums` and "Online Automatic Block Repair".

• KingbaseES Online Object Redefinition: 
  The KingbaseES database supports online logical or physical reorganization and redefinition of database objects without the need to create new table structures for import and export.

.. seealso:: 

   For more information about online database object redefinition, please refer to "Online Data Definition Change Feature".


• KingbaseES Data Export and Import, Data Migration Tools: 
  The KingbaseES database supports parallel data export and import, as well as data migration between homogeneous and heterogeneous databases using migration tools.

.. seealso:: 

   For more information about data export and import, please refer to `sys_dump` and `sys_restore`.

   For more information about data migration tools, please refer to "KDTS Migration Tool User Guide".
