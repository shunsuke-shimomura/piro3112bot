from discord.ext import commands
import datetime
import pickle
import os

class GuildData:
    def __init__(self, guild):
        print(guild.name)
        self.guild = guild
        self.exp_total = {}
        self.calling_duration_current = {}
        self.calling_duration_total = {}
        self.exp_filepath = os.path.join(os.getcwd(), guild.name + "exp.pkl")
        self.duration_filepath = os.path.join(os.getcwd(), guild.name + "duration.pkl")
        if(os.path.isfile(self.exp_filepath)):
            with open(self.exp_filepath, "rb") as tf:
                self.exp_total = pickle.load(tf)
        if(os.path.isfile(self.duration_filepath)):
            with open(self.duration_filepath, "rb") as tf:
                self.calling_duration_total = pickle.load(tf)

    def update_call_duration_current(self, member_name, point):
        if(member_name not in self.calling_duration_current.keys()):
            self.calling_duration_current[member_name] = [{"time": datetime.datetime.now(), "point":point}]
        else:
            self.calling_duration_current[member_name].append({"time": datetime.datetime.now(), "point":point})
        if (point == None):
            return self.fin(member_name)
        else:
            return None

    def fin(self, member_name):
        print(self.calling_duration_current[member_name])
        exp_current = 0
        pre_time_stamp = None

        if(member_name not in self.calling_duration_total.keys()):
            self.calling_duration_total[member_name] = 0
        for time_stamp in self.calling_duration_current[member_name]:
            if(pre_time_stamp != None):
                exp_current += int((time_stamp["time"] - pre_time_stamp["time"]).total_seconds()) * pre_time_stamp["point"]
                self.calling_duration_total[member_name] += (time_stamp["time"] - pre_time_stamp["time"]).total_seconds()
            pre_time_stamp = time_stamp

        calling_duration_current_total = (self.calling_duration_current[member_name][-1]["time"] - self.calling_duration_current[member_name][0]["time"]).total_seconds()
        if(member_name not in self.exp_total.keys()):
            self.exp_total[member_name] = exp_current // 60
        else:
            self.exp_total[member_name] += exp_current // 60
        del self.calling_duration_current[member_name]

        print(self.exp_total[member_name])
        print(self.calling_duration_total[member_name])
        print(calling_duration_current_total)

        if (calling_duration_current_total > 300):
            text_log = member_name + "???" 
            if(int(calling_duration_current_total // 3600) != 0):
                text_log += str(int(calling_duration_current_total // 3600)) + "??????"
            if(int(calling_duration_current_total % 3600 // 60)):
                text_log += str(int(calling_duration_current_total % 3600 // 60)) + "???" 
            text_log += str(int(calling_duration_current_total % 60)) + "?????????????????????"
            text_log += str(exp_current//60) + "?????????????????????"
        else:
            text_log = None
            self.save()
        return text_log

    def save(self):
        with open(self.exp_filepath, "wb") as tf:
            pickle.dump(self.exp_total,tf)
        with open(self.duration_filepath, "wb") as tf:
            pickle.dump(self.calling_duration_total,tf)

class Piro3112Bot(commands.Bot):

    async def on_ready(self):
        print('Logged on as {0}'.format(self.user))
        self.guild_data = {}
        for guild in self.guilds:
            self.guild_data[guild.name] = GuildData(guild)

    async def on_voice_state_update(self, member, before, after):
        if (member.bot):
            return
        point = 3
        if(after.deaf or after.self_deaf):
            point -= 3
        elif(after.mute or after.self_mute):
            point -= 1
        if(after.self_video or after.self_stream):
            point += 2
        if (after.channel == None):
            point = None
            
        text_log = self.guild_data[member.guild.name].update_call_duration_current(member.name, point)

        if(text_log != None):
            await member.guild.text_channels[0].send(text_log)

bot = Piro3112Bot(command_prefix="$")