repo: https://github.com/jschalk/jaar

![jaar logo](https://github.com/jschalk/jaar/tree/main/logo/jaar_64.png) jaar

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


JAAR Version 0.0.0

`jaar` is a python library for listening to the climate of a community.

## 0.0 About jaar

`jaar` is a python library for listening to the climate of a community. Individual 
positions are aggregated by a listener into a coherant agenda that can include pledges 
to do and pledges of states of existence. Listening and acting on it.

A agents's agenda in the community is built by the the massed intreprtation of
1. Acct agents agendas 
2. Their own independent agenda

Each agenda is saved as a JSON file. 

This is mostly a one man projeect. Femi has significantly helped. 

 
### 1.0 Installing `jaar`

<!-- TODO: add dependencies -->

Future enhancement: `jaar` can be installed using `pip`

<!-- TODO: Get pip install to function correctly

    pip install jaar

If you have installed `jaar` before, and you should ensure `pip` downloads the latest version (rather than using its internal cache) you can use the following commands:

    pip uninstall jaar
    pip install --no-cache jaar

-->

### 1.1 Hello 

<!-- TODO: Add simplest example

Should examples be found in a separate repository to ensure the `jaar` repository stays 
relatively small, whilst still providing a thorough knowledgebase of code-samples, 
screenshots and elucidatory text.

-->

## 1.2 Notes about data structure

<!-- TODO: Add elucidations -->
base attributes vs reason attributess

BudUnit objects

BudUnit AcctUnit objects

BudUnit GroupUnit objects

BudUnit ItemUnit objects

BudUnit ItemUnit hierarchical structure

BudUnit ItemUnit AwardLink objects

BudUnit ItemUnit AwardLine objects

BudUnit ItemUnit AwardHeir objects

BudUnit ItemUnit AwardHeir objects

BudUnit ItemUnit Reason PremiseUnit objects

BudUnit ItemUnit Reason PremiseHeir objects

BudUnit ItemUnit FactUnit objects

BudUnit ItemUnit FactHeir objects1


## 1.3 Test-Driven-Development

Jaar was developed using Test-Driven-Development so every feature should have a test. 
Tests can be hard to comprehend. Some tests have many variables and can be hard to follow.

<!-- TODO: Add examples 
Should examples be in a separate repository to ensure the `jaar` repository stays 
relatively small? (whilst still providing a thorough knowledgebase of code-samples, 
screenshots and elucidatory text.)
-->



## 2. License

<!-- TODO: Consider which license to pick -->


## 3. Acknowledgements

<!-- TODO: Consider which license to pick -->





<!-- TODO: Find out how to autopopulate the below modeled after the borb library
[![Corpus Coverage : 100.0%](https://img.shields.io/badge/corpus%20coverage-100.0%25-green)]()
[![Public Method Documentation : 100%](https://img.shields.io/badge/public%20method%20documentation-100%25-green)]()
[![Number of Tests : 615](https://img.shields.io/badge/number%20of%20tests-615-green)]()
[![Python : 3.8 | 3.9 | 3.10 ](https://img.shields.io/badge/python-3.8%20&#124;%203.9%20&#124;%203.10-green)]() 

[![Downloads](https://pepy.tech/badge/borb)](https://pepy.tech/projeect/borb)
[![Downloads](https://pepy.tech/badge/borb/month)](https://pepy.tech/projeect/borb)
-->



PUT conflicts in 

x_dict = {
    "bud_acct_membership":          {"jkeys": {"acct_name","group_label"},       "jvalues": {"credit_vote","debtit_vote"},
    "bud_acctunit":                 {"jkeys": {"acct_name",},                 "jvalues": {"credit_belief","debtit_belief"},
each idea will either have bud_acctunit as a dimen or not. that will decide if the atom is created. 
    "bud_item_awardlink":           {"jkeys": {"way","group_label",},         "jvalues": {"give_force","take_force"},
    "bud_item_teamlink":            {"jkeys": {"way","group_label",},         "jvalues",
each idea will either have bud_item_teamlink as a dimen or not. that will decide if the atom is created. 
    "bud_item_factunit":            {"jkeys": {"way","base",},             "jvalues": {"fnigh","fopen","pick",},},
each idea will either have bud_item_factunit as a dimen or not. Would be nice if pick was required...not required for delete
    "bud_item_reason_premiseunit":  {"jkeys": {"way","base","need",},      "jvalues": {"divisor","nigh","open",},},
    "bud_item_reasonunit":          {"jkeys": {"way","base",},             "jvalues": {"base_item_active_requisite",},},
}
