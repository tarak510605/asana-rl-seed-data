"""
Configuration management for the Asana seed data generator.
Loads settings from config.ini file.
"""
import configparser
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration manager that loads settings from config.ini"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration from config.ini file.
        
        Args:
            config_path: Path to config.ini file. If None, uses default location.
        """
        if config_path is None:
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config.ini"
        
        self.config = configparser.ConfigParser()
        
        if os.path.exists(config_path):
            self.config.read(config_path)
        else:
            # Use default values if config file not found
            self._set_defaults()
    
    def _set_defaults(self):
        """Set default configuration values"""
        self.config['database'] = {
            'output_path': 'output/asana_simulation.sqlite'
        }
        self.config['generation_counts'] = {
            'organizations': '1',
            'teams_per_org': '8',
            'users_per_org': '50',
            'projects_per_team': '4',
            'tasks_per_project': '20',
            'tags_count': '15'
        }
        self.config['generation_probabilities'] = {
            'task_unassigned_rate': '0.20',
            'task_has_due_date_rate': '0.70',
            'task_completion_rate': '0.70',
            'task_overdue_chance': '0.20',
            'subtask_probability': '0.30',
            'task_has_description_rate': '0.30',
            'task_has_tags_rate': '0.60',
            'custom_field_value_rate': '0.70'
        }
        self.config['date_ranges'] = {
            'org_created_days_ago_min': '730',
            'org_created_days_ago_max': '365',
            'team_created_days_ago_min': '365',
            'team_created_days_ago_max': '180',
            'user_created_days_ago_min': '365',
            'user_created_days_ago_max': '30',
            'project_created_days_ago_min': '300',
            'project_created_days_ago_max': '30',
            'task_created_days_ago_min': '200',
            'task_created_days_ago_max': '1'
        }
        self.config['logging'] = {
            'log_level': 'INFO',
            'log_to_file': 'false',
            'log_file_path': 'logs/generator.log'
        }
    
    def get(self, section: str, key: str, fallback: Any = None) -> str:
        """Get a configuration value"""
        return self.config.get(section, key, fallback=fallback)
    
    def getint(self, section: str, key: str, fallback: int = None) -> int:
        """Get an integer configuration value"""
        return self.config.getint(section, key, fallback=fallback)
    
    def getfloat(self, section: str, key: str, fallback: float = None) -> float:
        """Get a float configuration value"""
        return self.config.getfloat(section, key, fallback=fallback)
    
    def getboolean(self, section: str, key: str, fallback: bool = None) -> bool:
        """Get a boolean configuration value"""
        return self.config.getboolean(section, key, fallback=fallback)
    
    @property
    def db_output_path(self) -> str:
        """Get the database output path"""
        return self.get('database', 'output_path', 'output/asana_simulation.sqlite')
    
    @property
    def organizations_count(self) -> int:
        """Get number of organizations to generate"""
        return self.getint('generation_counts', 'organizations', 1)
    
    @property
    def teams_per_org(self) -> int:
        """Get number of teams per organization"""
        return self.getint('generation_counts', 'teams_per_org', 8)
    
    @property
    def users_per_org(self) -> int:
        """Get number of users per organization"""
        return self.getint('generation_counts', 'users_per_org', 50)
    
    @property
    def projects_per_team(self) -> int:
        """Get number of projects per team"""
        return self.getint('generation_counts', 'projects_per_team', 4)
    
    @property
    def tasks_per_project(self) -> int:
        """Get number of tasks per project"""
        return self.getint('generation_counts', 'tasks_per_project', 20)
    
    @property
    def tags_count(self) -> int:
        """Get number of tags to create"""
        return self.getint('generation_counts', 'tags_count', 15)


# Global config instance
_config = None

def get_config() -> Config:
    """Get the global configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config
