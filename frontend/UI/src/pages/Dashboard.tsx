import React from 'react';
import { Card, Descriptions, Tag, Button, Space, Typography, Avatar } from 'antd';
import { UserOutlined, LogoutOutlined, ProjectOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const { Title, Text } = Typography;

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleNavigateToKanban = () => {
    navigate('/kanban');
  };

  const getRoleTag = (roleName: string, hierarchyLevel: number) => {
    const roleColors: { [key: string]: string } = {
      'Admin': 'red',
      'Analyst': 'blue',
      'Partner': 'green',
    };

    return (
      <Tag color={roleColors[roleName] || 'default'} style={{ fontSize: 14, padding: '4px 12px' }}>
        {roleName} (Level {hierarchyLevel})
      </Tag>
    );
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (!user) {
    return null;
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '40px 20px'
    }}>
      <div style={{ maxWidth: 900, margin: '0 auto' }}>
        <Card
          style={{
            borderRadius: '12px',
            boxShadow: '0 10px 40px rgba(0,0,0,0.2)'
          }}
        >
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            {/* Header */}
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: '16px'
            }}>
              <Space>
                <Avatar size={64} icon={<UserOutlined />} style={{ backgroundColor: '#667eea' }} />
                <div>
                  <Title level={3} style={{ margin: 0 }}>
                    Welcome back{user.first_name ? `, ${user.first_name}` : ''}!
                  </Title>
                  <Text type="secondary">Here's your account information</Text>
                </div>
              </Space>
              <Space>
                <Button
                  type="primary"
                  icon={<ProjectOutlined />}
                  onClick={handleNavigateToKanban}
                  size="large"
                  style={{ backgroundColor: '#667eea', borderColor: '#667eea' }}
                >
                  Kanban
                </Button>
                <Button
                  danger
                  icon={<LogoutOutlined />}
                  onClick={handleLogout}
                  size="large"
                >
                  Logout
                </Button>
              </Space>
            </div>

            {/* User Information */}
            <Card 
              title="User Information" 
              type="inner"
              style={{ borderRadius: '8px' }}
            >
              <Descriptions column={1} bordered>
                <Descriptions.Item label="User ID">
                  <strong>{user.id}</strong>
                </Descriptions.Item>
                <Descriptions.Item label="Email">
                  <strong>{user.email}</strong>
                </Descriptions.Item>
                <Descriptions.Item label="Username">
                  <strong>{user.username}</strong>
                </Descriptions.Item>
                {user.first_name && (
                  <Descriptions.Item label="First Name">
                    <strong>{user.first_name}</strong>
                  </Descriptions.Item>
                )}
                {user.last_name && (
                  <Descriptions.Item label="Last Name">
                    <strong>{user.last_name}</strong>
                  </Descriptions.Item>
                )}
                <Descriptions.Item label="Account Created">
                  <strong>{formatDate(user.created_at)}</strong>
                </Descriptions.Item>
              </Descriptions>
            </Card>

            {/* Role Information */}
            {user.role && (
              <Card 
                title="Role & Permissions" 
                type="inner"
                style={{ borderRadius: '8px' }}
              >
                <Descriptions column={1} bordered>
                  <Descriptions.Item label="Role">
                    {getRoleTag(user.role.name, user.role.hierarchy_level)}
                  </Descriptions.Item>
                  <Descriptions.Item label="Hierarchy Level">
                    <strong>{user.role.hierarchy_level}</strong>
                  </Descriptions.Item>
                  <Descriptions.Item label="Permissions">
                    {user.role.permissions.length > 0 ? (
                      <Space wrap>
                        {user.role.permissions.map((permission, index) => (
                          <Tag key={index} color="blue">{permission}</Tag>
                        ))}
                      </Space>
                    ) : (
                      <Text type="secondary">No specific permissions assigned</Text>
                    )}
                  </Descriptions.Item>
                </Descriptions>

                {/* Role Description */}
                <div style={{ marginTop: 24, padding: '16px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                  <Text strong>Role Capabilities:</Text>
                  <ul style={{ marginTop: 8, marginBottom: 0 }}>
                    {user.role.name === 'Admin' && (
                      <>
                        <li>Manage users and assign roles</li>
                        <li>Full access to all deals and IC memos</li>
                        <li>Can perform all actions in the system</li>
                      </>
                    )}
                    {user.role.name === 'Analyst' && (
                      <>
                        <li>Create and edit deals</li>
                        <li>Create and edit IC memos</li>
                        <li>Move deals through pipeline stages</li>
                      </>
                    )}
                    {user.role.name === 'Partner' && (
                      <>
                        <li>View deals and IC memos</li>
                        <li>Comment on deals</li>
                        <li>Vote to approve or decline deals</li>
                      </>
                    )}
                  </ul>
                </div>
              </Card>
            )}
          </Space>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;

