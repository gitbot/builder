module.exports  = {
    development: false,
    production: true,
    staging: false,
    logLevel: 'info',
    site: 'http://{ "Ref": "Domain" }',
    hookReceiver: 'http://api.{ "Ref": "Domain" }/hooks/{project}/action/{event}',
    statusReceiver: 'http://api.{ "Ref": "Domain" }/job/{jobId}/status',
    db: {
        host: '{ "Fn::GetAtt": ["RedisServer", "Outputs.MasterIP"] }',
        port: '{ "Ref" : "RedisPort" }'
    },
    q: {
        host: '{ "Fn::GetAtt": ["RedisServer", "Outputs.MasterIP"] }',
        port: '{ "Ref" : "RedisPort" }'
    },
    api: {
        ip: '127.0.0.1',
        port: '3000',
        url: 'http://api.{ "Ref": "Domain" }'
    },
    queue: {
        ip: '127.0.0.1',
        port: '3001',
        url: 'http://kue.{ "Ref": "Domain" }'
    },
    socket: {
        origins: '*:*, localhost:8181, { "Ref": "Domain"}'
    },
    auth: {
        clientId: '{ "Ref": "GithubClientId" }',
        clientSecret: '{ "Ref": "GithubClientSecret" }'
    },
    worker: {
        region: '{ "Ref": "AWS::Region" }',
        queueUrl: '{ "Ref": "WorkerQueueURL" }',
        managerKey: '{ "Ref": "ManagerAccessKey" }',
        managerSecret: '{ "Ref": "ManagerSecretKey" }'
    }
};
