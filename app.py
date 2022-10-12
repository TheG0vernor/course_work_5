from flask import Flask, render_template, request, redirect

from dao.basic.base import Arena
from dao.basic.unit import PlayerUnit, EnemyUnit, BaseUnit
from dao.classes import unit_classes
from dao.equipment import Equipment

app = Flask(__name__)

heroes: dict = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    """Главное меню игры"""
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    """Экран начала боя"""
    arena.start_game(heroes['player'], heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    """Экран сражения"""
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result
    return render_template('fight.html', result=result, heroes=heroes)


@app.route("/fight/use-skill")
def use_skill():
    """Кнопка использования умения"""
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result
    return render_template('fight.html', result=result, heroes=heroes)


@app.route("/fight/pass-turn")
def pass_turn():
    """Кнопка пропуска хода"""
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result
    return render_template('fight.html', result=result, heroes=heroes)


@app.route("/fight/end-fight")
def end_fight():
    """Кнопка завершения игры"""
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """Экран выбора героя"""
    equipment = Equipment()
    if request.method == 'GET':
        weapon = equipment.get_weapons_names()
        armor = equipment.get_armors_names()
        classes = unit_classes

        result = {"header": "Выберите героя",
                  "armors": armor,
                  "weapons": weapon,
                  "classes": classes}
        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        name = request.form['name']
        weapon = request.form['weapon']
        armor = request.form['armor']
        unit_class = request.form['unit_class']

        player = PlayerUnit(name=name, unit_class=unit_classes[unit_class])
        player.equip_armor(equipment.get_armor(armor))
        player.equip_weapon(equipment.get_weapon(weapon))
        heroes['player'] = player
        return redirect("/choose-enemy/")


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """Экран выбора противника"""
    equipment = Equipment()
    if request.method == 'GET':
        weapon = equipment.get_weapons_names()
        armor = equipment.get_armors_names()
        classes = unit_classes

        result = {"header": "Выберите противника",
                  "armors": armor,
                  "weapons": weapon,
                  "classes": classes}
        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        name = request.form['name']
        weapon = request.form['weapon']
        armor = request.form['armor']
        unit_class = request.form['unit_class']

        enemy = EnemyUnit(name=name, unit_class=unit_classes[unit_class])
        enemy.equip_armor(equipment.get_armor(armor))
        enemy.equip_weapon(equipment.get_weapon(weapon))
        heroes['enemy'] = enemy
        return redirect("/fight/")
        # также можно делать редирект по имени функции:
        # redirect(url_for("start_fight"))


if __name__ == "__main__":
    app.run()
