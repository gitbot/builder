module.exports  = {
    development: false,
    production: true,
    staging: false,
    logLevel: 'info',
    site: 'http://{ "Ref": "Domain" }',
    hookReceiver: 'http://api.{ "Ref": "Domain" }/hooks',
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
        origins: '*:*, localhost:8181'
    },
    auth: {
        clientId: '{ "Ref": "GithubClientId" }',
        clientSecret: '{ "Ref": "GithubClientSecret" }'
    }
};
