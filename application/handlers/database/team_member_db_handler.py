from __future__ import annotations

from application.handlers.database.base_db_handler import BaseDBHandler
from application.handlers.database.models import TeamMember
from application.utils.logger import Logger


class TeamMemberDBHandler(BaseDBHandler):
    def __init__(self):
        super().__init__(TeamMember)
        self.logger = Logger.get_logger()

    def add_user_to_team(self, user_id, team_id, is_manager):
        current_user_team_id = self.get_team_member_by_user_id(user_id).id
        is_added_in_this_team = current_user_team_id and current_user_team_id == team_id
        is_added_in_other_team = current_user_team_id and current_user_team_id != team_id
        if is_added_in_other_team:
            self.logger.error(f'Exist in other team {team_id}')
        if is_added_in_this_team:
            self.logger.info('Added in this team')
        self.add_item({
            'user_id': user_id,
            'team_id': team_id,
            'is_manager': is_manager,
        })

    def remove_user_to_team(self, user_id, team_id):
        self.execute(
            self.table.delete()
                .where(self.table.c.user_id == user_id)
                .where(self.table.c.role_id == team_id),
        )

    def get_team_managers_by_team_id(self, team_id):
        result = self.execute(
            self.table.select()
                .filter(
                self.table.team_id == team_id,
                self.table.is_manager == 1,
                ),
        )
        return result.all() if result.rowcount else []

    def get_all_team_members_by_team_id(self, team_id):
        result = self.execute(
            self.table.select()
                .filter(
                self.table.team_id == team_id,
                ),
        )
        return result.all() if result.rowcount else []

    def get_team_member_by_user_id(self, user_id):
        result = self.execute(
            self.table.select()
                .filter(
                self.table.user_id == user_id,
                ),
        )
        return result.first() if result.rowcount else None
