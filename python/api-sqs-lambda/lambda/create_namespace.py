import json
import boto3


from variables import aws_account_id

def handler(event, context):
    print('create_namespace')
    client = boto3.client('quicksight')
    namespace_name=event['body']
    
    response_create_namespace = client.create_namespace(
        AwsAccountId=aws_account_id,
        Namespace=namespace_name,
        IdentityStore='QUICKSIGHT',
        Tags=[
            {
                'Key': 'NamespaceTest',
                'Value': 'This is a namespace test tag'
            },
        ]
    )
    print('response_create_namespace',response_create_namespace)

    # iterate through namespaces to retrieve ARN for folder owner
    # response_list_namespaces = client.list_namespaces(
    #     AwsAccountId='331992388334',
    #     MaxResults=99
    # )
    # print('response_list_namespaces',response_list_namespaces)
    
    # create a folder for the namespace - namespace must be one of the principals
    # if you do not define a principal and actions for the principal, the asset will be created but no one will see it in the UI!
    response_create_folder = client.create_folder(
        AwsAccountId=aws_account_id,
        FolderId=namespace_name,
        Name=namespace_name,
        FolderType='SHARED',
        Permissions=[
            {
            'Principal': 'arn:aws:quicksight:us-east-1:331992388334:user/default/Administrator',
            'Actions': [
                "quicksight:CreateFolder",
                "quicksight:DescribeFolder", 
                "quicksight:UpdateFolder",
                "quicksight:DeleteFolder",
                "quicksight:CreateFolderMembership",
                "quicksight:DeleteFolderMembership",
                "quicksight:DescribeFolderPermissions",
                "quicksight:UpdateFolderPermissions"
                ]
            },
        ],
        Tags=[
            {
                'Key': 'FolderTest',
                'Value': 'this is a folder test tag'
            },
        ]
    )
    print('response_create_folder',response_create_folder)

    
    # iterate through templates to find the ones chosen in the portal for the tenant
    # response_list_templates = client.list_templates(
    #     AwsAccountId=aws_account_id,
    #     MaxResults=99
    #     )
    # print('response_list_templates',response_list_templates)
    
    # will need to create one dashboard for each chosen template - namespace must be one of the principals 
    # if you do not define a principal and actions for the principal, the asset will be created but no one will see it in the UI!
    response_create_dashboard = client.create_dashboard(
    AwsAccountId=aws_account_id,
    DashboardId=namespace_name+'_Activity_Report',
    Name='Daily Activity Report',
    Permissions=[
        {
            'Principal': 'arn:aws:quicksight:us-east-1:331992388334:user/default/Administrator',
            'Actions': [
                "quicksight:DescribeDashboard", 
                "quicksight:ListDashboardVersions", 
                "quicksight:UpdateDashboardPermissions", 
                "quicksight:QueryDashboard", 
                "quicksight:UpdateDashboard", 
                "quicksight:DeleteDashboard", 
                "quicksight:DescribeDashboardPermissions", 
                "quicksight:UpdateDashboardPublishedVersion"
            ]
        },
    ],
    SourceEntity={
        'SourceTemplate': {
            'DataSetReferences': [
                {
                    'DataSetPlaceholder': 'TestTemplate1Dataset',
                    'DataSetArn': 'arn:aws:quicksight:us-east-1:331992388334:dataset/9a76a1f4-5d90-44c3-af79-e0e5fa14b8f3'
                },
            ],
            'Arn': 'arn:aws:quicksight:us-east-1:331992388334:template/TestTemplate1'
        }
    },
    Tags=[
        {
            'Key': 'TestTemplateTag',
            'Value': 'This is a test template tag'
        },
    ],
    )
    print('response_create_dashboard',response_create_dashboard)
    
    # iterate through the chosen list and place dashboard(s) in the tenant folder 
    response_create_folder_membership = client.create_folder_membership(
        AwsAccountId=aws_account_id,
        FolderId=namespace_name,
        MemberId=namespace_name+'_Activity_Report',
        MemberType='DASHBOARD'
    )
    print('response_create_folder_membership',response_create_folder_membership)