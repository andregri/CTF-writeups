Java.perform(function()
{
	// Simple script the constructor -> new()
	
	var ig = Java.use("ig");
	
	ig.$init.overload("android.content.Context").implementation = function(context)
	{
		console.log("[+]\t Constructor of ig hooked!");
		
		var res = this.a();
		console.log("[+]\t this.a() = " + res);
		
		console.log("[+]\t this.c = " + JSON.stringify(this.c));
		
		Java.choose('ig', {
			onMatch: function(instance) {
				console.log("[+]\t Istance of ig.c = " + instance.c.value);
			},
			onComplete: function() {}
		});
		
		return this.$init(context);
	}
})

Java.perform(function () {
  var Activity = Java.use('android.app.Activity');
  Activity.onResume.implementation = function () {
    send('onResume() got called! Let\'s call the original implementation');
    this.onResume();
	
	var ig = Java.use("ig");
	var context = Java.use('android.app.ActivityThread').currentApplication().getApplicationContext();
	ig.$new(context);
  };
});