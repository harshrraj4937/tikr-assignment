import React, { useState, useEffect } from 'react';
import { Modal, List, Typography, Space, Tag, Avatar, Button, Empty, Spin } from 'antd';
import { EyeOutlined, UserOutlined, ClockCircleOutlined, EditOutlined } from '@ant-design/icons';
import { icMemoAPI } from '../services/api';
import type { ICMemo } from '../types/icmemo';

const { Title, Text } = Typography;

interface ICMemoVersionHistoryProps {
  dealId: number;
  dealName: string;
  open: boolean;
  onClose: () => void;
  onViewVersion: (version: number) => void;
  onEditNew?: () => void;
}

const ICMemoVersionHistory: React.FC<ICMemoVersionHistoryProps> = ({
  dealId,
  dealName,
  open,
  onClose,
  onViewVersion,
  onEditNew,
}) => {
  const [memos, setMemos] = useState<ICMemo[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open && dealId) {
      loadVersionHistory();
    }
  }, [open, dealId]);

  const loadVersionHistory = async () => {
    try {
      setLoading(true);
      const data = await icMemoAPI.listMemoVersions(dealId);
      setMemos(data);
    } catch (error: any) {
      console.error('Error loading version history:', error);
      setMemos([]);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getVersionColor = (version: number, isLatest: boolean) => {
    if (isLatest) return '#52c41a';
    return '#8b5cf6';
  };

  return (
    <Modal
      title={
        <Space direction="vertical" size={0}>
          <Title level={3} style={{ margin: 0 }}>
            Version History
          </Title>
          <Text type="secondary">{dealName}</Text>
        </Space>
      }
      open={open}
      onCancel={onClose}
      width={700}
      footer={
        <Space style={{ width: '100%', justifyContent: 'space-between' }}>
          <Button onClick={onClose} size="large">
            Close
          </Button>
          {onEditNew && (
            <Button
              type="primary"
              icon={<EditOutlined />}
              onClick={onEditNew}
              size="large"
              style={{ background: '#667eea' }}
            >
              Create New Version
            </Button>
          )}
        </Space>
      }
      destroyOnClose
    >
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px 0' }}>
          <Spin size="large" />
        </div>
      ) : memos.length > 0 ? (
        <List
          itemLayout="horizontal"
          dataSource={memos}
          style={{ maxHeight: '60vh', overflowY: 'auto' }}
          renderItem={(memo, index) => {
            const isLatest = index === 0;
            const authorName = memo.created_by.first_name && memo.created_by.last_name
              ? `${memo.created_by.first_name} ${memo.created_by.last_name}`
              : memo.created_by.username;

            return (
              <List.Item
                key={memo.id}
                style={{
                  padding: '20px',
                  marginBottom: 12,
                  background: isLatest ? '#f0f9ff' : '#fafafa',
                  borderRadius: '8px',
                  border: isLatest ? '2px solid #667eea' : '1px solid #e8e8e8',
                }}
                actions={[
                  <Button
                    type="link"
                    icon={<EyeOutlined />}
                    onClick={() => onViewVersion(memo.version)}
                  >
                    View
                  </Button>,
                ]}
              >
                <List.Item.Meta
                  avatar={
                    <div style={{ position: 'relative' }}>
                      <Avatar
                        size={48}
                        style={{
                          backgroundColor: getVersionColor(memo.version, isLatest),
                        }}
                      >
                        {memo.version}
                      </Avatar>
                      {isLatest && (
                        <Tag
                          color="success"
                          style={{
                            position: 'absolute',
                            bottom: -8,
                            left: '50%',
                            transform: 'translateX(-50%)',
                            fontSize: 10,
                            padding: '0 4px',
                          }}
                        >
                          Latest
                        </Tag>
                      )}
                    </div>
                  }
                  title={
                    <Space direction="vertical" size={4}>
                      <Text strong style={{ fontSize: 16 }}>
                        Version {memo.version}
                      </Text>
                      <Space size={8}>
                        <Space size={4}>
                          <UserOutlined style={{ color: '#999' }} />
                          <Text type="secondary">{authorName}</Text>
                        </Space>
                        <Text type="secondary">•</Text>
                        <Space size={4}>
                          <ClockCircleOutlined style={{ color: '#999' }} />
                          <Text type="secondary">{formatDate(memo.created_at)}</Text>
                        </Space>
                      </Space>
                    </Space>
                  }
                  description={
                    <div style={{ marginTop: 8 }}>
                      <Text type="secondary">
                        {memo.sections.summary
                          ? memo.sections.summary.substring(0, 120) +
                            (memo.sections.summary.length > 120 ? '...' : '')
                          : 'No summary provided'}
                      </Text>
                    </div>
                  }
                />
              </List.Item>
            );
          }}
        />
      ) : (
        <Empty
          description="No IC Memo versions yet"
          style={{ padding: '60px 0' }}
          image={Empty.PRESENTED_IMAGE_SIMPLE}
        >
          {onEditNew && (
            <Button
              type="primary"
              icon={<EditOutlined />}
              onClick={onEditNew}
              size="large"
              style={{ background: '#667eea' }}
            >
              Create First Version
            </Button>
          )}
        </Empty>
      )}
    </Modal>
  );
};

export default ICMemoVersionHistory;

