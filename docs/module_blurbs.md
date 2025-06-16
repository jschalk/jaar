# Module Overview

What does each one do?

- **a00_data_toolbox**: Creates a set of tools for data manipulation and analysis.
- **a01_term_logic**: Defines the terms and concepts used in the system for consistent understanding and processing.
- **a02_finance_logic**: Defines financial rules and calculations to ensure accurate financial operations.
- **a03_group_logic**: Defines accounts, account memberships, and groups. Groups will be produced from memberships.
- **a04_reason_logic**: Describes what a reason and a fact is; if the reasons match the facts, then a task can be kept.
- **a05_concept_logic**: A concept can be a task, and if its reasons match its facts, it should be kept.
- **a06_plan_logic**: A plan is a planget, made of accounts and concepts. All concepts are connected to the axiom concept, which is given all the funds in a planget.
- **a07_calendar_logic**: Allows arbitrary calendars to be defined for each planget with minimal configuration.
- **a08_plan_atom_logic**: Defines the structure and behavior of planget atoms, which are single units of planget and concepts used in a planget.
- **a09_pack_logic**: Manages the creation and organization of packs, which are collections of planget atoms for building complex plangets.
- **a10_plan_calc**: Expresses the calculations performed when a planget is "settled" to determine final amounts for each concept and account.
- **a11_bud_cell_logic**: When a vow system decides to empower a planget the funds must be distributed
- **a12_hub_tools**: These tools are used to handle complex operations involving plan files, will be deprecated.
- **a13_plan_listen_logic**: These tools describe how one planget listens to another
- **a14_keep_logic**: Builds a simulation that describes how much credit a healer has earned 
- **a15_vow_logic**: A VowUnit is a Vow system with the basic requirements: common system of time, acct tranactions ledger, etc. Importantly a Vow system must know the state of a owner's planget at any time in the past. 
- **a16_pidgin_logic**: A tool that translates words from outside language to inside language.  
- **a17_idea_logic**: idea bricks are tables of data that build vow systems and the plangets within them.
- **a18_etl_toolbox**: 
- **a19_world_logic**: *(description needed)*
- **a20_lobby_logic**: *(description needed)*