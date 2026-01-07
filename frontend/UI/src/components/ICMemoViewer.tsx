import React, { useState, useEffect } from 'react';
import { Modal, Typography, Divider, Space, Tag, Avatar, Spin, Button } from 'antd';
import { ArrowLeftOutlined, UserOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import { icMemoAPI } from '../services/api';
import type { ICMemo, ICMemoSections } from '../types/icmemo';
import { MEMO_SECTION_LABELS } from '../types/icmemo';

const { Title, Text, Paragraph } = Typography;

interface ICMemoViewerProps {
  dealId: number;
  dealName: string;
  version: number;
  open: boolean;
  onClose: () => void;
}

const ICMemoViewer: React.FC<ICMemoViewerProps> = ({
  dealId,
  dealName,
  version,
  open,
  onClose,
}) => {
  const [memo, setMemo] = useState<ICMemo | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open && dealId && version) {
      loadMemo();
    }
  }, [open, dealId, version]);

  const loadMemo = async () => {
    try {
      setLoading(true);
      const data = await icMemoAPI.getMemoVersion(dealId, version);
      setMemo(data);
    } catch (error: any) {
      console.error('Error loading memo:', error);
      setMemo(null);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const sectionKeys: (keyof ICMemoSections)[] = [
    'summary',
    'market',
    'product',
    'traction',
    'risks',
    'open_questions',
  ];

  return (
    <Modal
      title={
        <Space direction="vertical" size={4}>
          <Title level={3} style={{ margin: 0 }}>
            {dealName} - Version {version}
          </Title>
          <Space>
            <Tag color="orange">Read-Only</Tag>
            {memo && (
              <>
                <Text type="secondary">
                  Created by {memo.created_by.first_name || memo.created_by.username}
                </Text>
                <Text type="secondary">•</Text>
                <Text type="secondary">{formatDate(memo.created_at)}</Text>
              </>
            )}
          </Space>
        </Space>
      }
      open={open}
      onCancel={onClose}
      width={900}
      footer={
        <Button icon={<ArrowLeftOutlined />} onClick={onClose} size="large">
          Back
        </Button>
      }
      destroyOnClose
    >
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px 0' }}>
          <Spin size="large" />
        </div>
      ) : memo ? (
        <div style={{ maxHeight: '70vh', overflowY: 'auto', padding: '0 8px' }}>
          {sectionKeys.map((key, index) => (
            <div key={key}>
              {index > 0 && <Divider style={{ margin: '32px 0' }} />}
              <div style={{ marginBottom: 24 }}>
                <Title level={4} style={{ color: '#667eea', marginBottom: 8 }}>
                  {MEMO_SECTION_LABELS[key]}
                </Title>
                <div
                  style={{
                    background: '#f5f5f5',
                    padding: '16px 20px',
                    borderRadius: '8px',
                    borderLeft: '4px solid #667eea',
                  }}
                >
                  {memo.sections[key] ? (
                    <div style={{ fontSize: 14, lineHeight: 1.6 }}>
                      <ReactMarkdown>{memo.sections[key]}</ReactMarkdown>
                    </div>
                  ) : (
                    <Text type="secondary" italic>
                      No content provided
                    </Text>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '60px 0' }}>
          <Text type="secondary">Memo not found</Text>
        </div>
      )}
    </Modal>
  );
};

export default ICMemoViewer;

