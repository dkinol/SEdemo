window.App = Ember.Application.create();

App.Router = Ember.Router.extend({
	rootURL: '/pa3/live'
});

App.Store = DS.Store.extend({});

App.ApplicationAdapter = DS.JSONAPIAdapter.extend({
	namespace: '/pa3/api/v1'
})
