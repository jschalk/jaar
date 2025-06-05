# Module Overview

What does each one do?

- **a00_data_toolbox**: Creates a set of tools for data manipulation and analysis.
- **a01_term_logic**: Defines the terms and concepts used in the system for consistent understanding and processing.
- **a02_finance_logic**: Defines financial rules and calculations to ensure accurate financial operations.
- **a03_group_logic**: Defines accounts, account memberships, and groups. Groups will be produced from memberships.
- **a04_reason_logic**: Describes what a reason and a fact is; if the reasons match the facts, then a pledge can be kept.
- **a05_concept_logic**: A concept can be a pledge, and if its reasons match its facts, it should be kept.
- **a06_bud_logic**: A bud is a budget, made of accounts and concepts. All concepts are connected to the axiom concept, which is given all the funds in a budget.
- **a07_calendar_logic**: Allows arbitrary calendars to be defined for each budget with minimal configuration.
- **a08_bud_atom_logic**: Defines the structure and behavior of budget atoms, which are single units of budget and concepts used in a budget.
- **a09_pack_logic**: Manages the creation and organization of packs, which are collections of budget atoms for building complex budgets.
- **a10_bud_calc**: Expresses the calculations performed when a budget is "settled" to determine final amounts for each concept and account.
- **a11_deal_cell_logic**: When a fiscal system decides to empower a budget the funds must be distributed
- **a12_hub_tools**: These tools are used to handle complex operations involving bud files, will be deprecated.
- **a13_bud_listen_logic**: These tools describe how one budget listens to another
- **a14_keep_logic**: Builds a simulation that describes how much credit a healer has earned 
- **a15_fisc_logic**: A FiscUnit is a Fiscal system with the basic requirements: common system of time, acct tranactions ledger, etc. Importantly a Fiscal system must know the state of a owner's budget at any time in the past. 
- **a16_pidgin_logic**: A tool that translates words from outside language to inside language.  
- **a17_idea_logic**: idea bricks are tables of data that build fiscal systems and the budgets within them.
- **a18_etl_toolbox**: 
- **a19_world_logic**: *(description needed)*
- **a20_lobby_logic**: *(description needed)*