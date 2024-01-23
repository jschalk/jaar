from src._prime.road import (
    create_road,
    create_economyaddress,
    PersonRoad,
    create_road_from_nodes as roadnodes,
)
from src.world.deal import dealunit_shop, DealUnit, vowunit_shop
from src.world.examples.example_topics import get_no_topiclinks_vowunit


def get_bob_personroad() -> PersonRoad:
    bob_text = "Bob"
    food_text = "Hunger"
    yao_text = "Yao"
    ohio_text = "Ohio"
    return roadnodes([bob_text, food_text, yao_text, ohio_text])


def get_sue_personroad() -> PersonRoad:
    sue_text = "Sue"
    food_text = "Hunger"
    yao_text = "Yao"
    ohio_text = "Ohio"
    return roadnodes([sue_text, food_text, yao_text, ohio_text])


def get_yao_personroad() -> PersonRoad:
    yao_text = "Yao"
    food_text = "Hunger"
    ohio_text = "Ohio"
    return roadnodes([yao_text, food_text, yao_text, ohio_text])


def get_no_topiclinks_yao_sue_dealunit() -> DealUnit:
    yao_sue_dealunit = dealunit_shop(get_yao_personroad(), get_sue_personroad())
    yao_sue_dealunit.set_vowunit(vowunit_shop(1, author_weight=12, reader_weight=7))
    yao_sue_dealunit.set_vowunit(vowunit_shop(1, author_weight=28, reader_weight=28))
    return yao_sue_dealunit