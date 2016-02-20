// /static/js/app/app.js
window.App = Ember.Application.create();
///5b97d6975c7441eb8778a/pa3
App.Router = Ember.Router.extend({ 
	rootURL: '/5b97d6975c7441eb8778a/pa3/live'
	//rootURL: '/live'
});

App.Store = DS.Store.extend({});

App.ApplicationAdapter = DS.JSONAPIAdapter.extend({
	namespace: '/5b97d6975c7441eb8778a/pa3/jsonapi/v1'
})

App.Router.map(function(){
	this.route('pic', {path: 'pic/:pic_id'});
})

App.Pic - DS.Model.extend({
	picurl: DS.attr('string'),
	prevpicid: DS.attr('string'),
	nextpicid: DS.attr('string'),
	caption: DS.attr('string'),
})

App.PicRoute = Ember.Route.Extend({
	model: function(params) {
		var pic = this.store.findRecord('pic',params.pic_id);
		return pic;
	},

	actions: {
		save: function(){
			var pic = this.modelFor('pic');
			var caption = this.modelFor('pic').get('caption');
			this.set('caption', caption);
			this.modelFor('pic').save();
		}
	},

	renderTemplate: function(){
		this.render('pic');
	}
});