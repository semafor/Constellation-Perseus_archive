YUI.add('vorsum-action-list', function (Y) {

    Y.VorsumActionList = Y.Base.create('actionList', Y.ModelList, [], {
        
        model: Y.VorsumActionModel,

        sync: Y.LocalStorageSync('actions'),


    });
});