class AnnouncementsOperation{constructor(idMapping,ip){this._idMapping=idMapping;this._ip=ip;this.deleteAnnouncement=this.deleteAnnouncement.bind(this);}
async deleteAnnouncement(index){if(confirm('確定要刪除這個公告？')){const targetId=this._idMapping[index].id;try{const url=`${this._ip}/announcement/${targetId}`;const res=await axios.delete(url);}catch(e){console.log(e);}
setTimeout(()=>{window.location.reload(true);},1000);}}}