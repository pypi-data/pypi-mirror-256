import time
from types import SimpleNamespace as SN

from autowsgr.constants import literals
from autowsgr.fight.battle import BattlePlan
from autowsgr.fight.exercise import NormalExercisePlan
from autowsgr.fight.normal_fight import NormalFightPlan
from autowsgr.game.game_operation import (
    Expedition,
    RepairByBath,
    SetSupport,
    get_rewards,
)
from autowsgr.scripts.main import start_script


class DailyOperation:
    def __init__(self, setting_path) -> None:
        self.timer = start_script(setting_path)

        self.config = SN(**self.timer.config.daily_automation)
        self.config.DEBUG = False
        self.complete_time = None

        if self.config.auto_expedition:
            self.expedition_plan = Expedition(self.timer)

        if self.config.auto_battle:
            self.battle_plan = BattlePlan(self.timer, plan_path=f"battle/{self.config.battle_type}.yaml")

        if self.config.auto_exercise:
            self.exercise_plan = NormalExercisePlan(self.timer, "exercise/plan_1.yaml")

        if self.config.auto_normal_fight:
            self.fight_plans = []
            self.fight_complete_times = []
            for plan in self.config.normal_fight_tasks:
                self.fight_plans.append(
                    NormalFightPlan(
                        self.timer,
                        plan_path=f"normal_fight/{plan[0]}.yaml",
                        fleet_id=plan[1],
                    )
                )
                self.fight_complete_times.append([0, plan[2]])  # 二元组， [已完成次数, 目标次数]

        self.start_time = self.last_time = time.time()

    def run(self):
        # 自动战役，直到超过次数
        if self.config.auto_battle:
            ret = literals.OPERATION_SUCCESS_FLAG
            while ret == literals.OPERATION_SUCCESS_FLAG:
                ret = self.battle_plan.run()

        # 自动开启支援
        if self.config.auto_set_support:
            SetSupport(self.timer, True)

        # 自动演习
        if self.config.auto_exercise:
            self.check_exercise()

        # 自动出征
        if self.config.auto_normal_fight:
            while self._has_unfinished():
                task_id = self._get_unfinished()

                plan = self.fight_plans[task_id]
                ret = plan.run()

                if ret == literals.OPERATION_SUCCESS_FLAG:
                    self.fight_complete_times[task_id][0] += 1
                elif ret == literals.DOCK_FULL_FLAG:
                    break  # 不解装则结束出征

                if time.time() - self.last_time >= 5 * 60:
                    self._expedition()
                    self._gain_bonus()
                    if self.config.auto_exercise:
                        self.check_exercise()
                    self.last_time = time.time()

        # 自动远征
        while True:
            self._bath_repair()
            if self.config.auto_exercise:
                self.check_exercise()
            self._expedition()
            self._gain_bonus()
            time.sleep(360)

    def _has_unfinished(self):
        return any(times[0] < times[1] for times in self.fight_complete_times)

    def _get_unfinished(self):
        for i, times in enumerate(self.fight_complete_times):
            if times[0] < times[1]:
                return i

    def _expedition(self):
        if self.config.auto_expedition:
            self.expedition_plan.run(True)

    def _gain_bonus(self):
        if self.config.auto_gain_bonus:
            get_rewards(self.timer)

    def _bath_repair(self):
        if self.config.auto_bath_repair:
            RepairByBath(self.timer)

    # 检查是否可以执行演习任务
    def check_exercise(self):
        # 判断在哪个时间段
        now_time = time.localtime(time.time())
        hour = now_time.tm_hour
        if 0 <= hour < 12:
            self.new_time_period = "0:00-12:00"
        elif 12 <= hour < 18:
            self.new_time_period = "12:00-18:00"
        else:
            self.new_time_period = "18:00-23:59"
        # 判断当前时间段是否执行过任务了
        if self.new_time_period != self.complete_time:
            self.timer.logger.info("即将执行演习任务")
            self.exercise_plan.run()
            self.complete_time = self.new_time_period
        else:
            self.timer.logger.info("当前时间段演习已完成")
