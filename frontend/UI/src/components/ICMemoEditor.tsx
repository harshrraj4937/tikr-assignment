import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Button, Space, Typography, Divider, message, Spin } from 'antd';
import { SaveOutlined, HistoryOutlined } from '@ant-design/icons';
import { icMemoAPI } from '../services/api';
import type { ICMemoSections, ICMemo } from '../types/icmemo';
import { MEMO_SECTION_LABELS, MEMO_SECTION_DESCRIPTIONS } from '../types/icmemo';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;

interface ICMemoEditorProps {
  dealId: number;
  dealName: string;
  open: boolean;
  onClose: () => void;
  onSaved?: () => void;
  onViewHistory?: () => void;
}

const ICMemoEditor: React.FC<ICMemoEditorProps> = ({
  dealId,
  dealName,
  open,
  onClose,
  onSaved,
  onViewHistory,
}) => {
  const [form] = Form.useForm();
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(false);
  const [latestVersion, setLatestVersion] = useState<number | null>(null);

  useEffect(() => {
    if (open) {
      loadLatestMemo();
    }
  }, [open, dealId]);

  const loadLatestMemo = async () => {
    try {
      setLoading(true);
      const memo = await icMemoAPI.getLatestMemo(dealId);
      form.setFieldsValue(memo.sections);
      setLatestVersion(memo.version);
    } catch (error: any) {
      // No memo exists yet, start fresh
      if (error.response?.status === 404) {
        form.resetFields();
        setLatestVersion(null);
      } else {
        message.error('Failed to load memo');
        console.error('Error loading memo:', error);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (values: ICMemoSections) => {
    try {
      setSaving(true);
      const newMemo = await icMemoAPI.createMemoVersion(dealId, { sections: values });
      message.success(`Saved as version ${newMemo.version}`);
      setLatestVersion(newMemo.version);
      onSaved?.();
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Failed to save memo');
      console.error('Error saving memo:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleClose = () => {
    form.resetFields();
    onClose();
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
        <Space direction="vertical" size={0}>
          <Title level={3} style={{ margin: 0 }}>
            IC Memo: {dealName}
          </Title>
          {latestVersion !== null && (
            <Text type="secondary">Current Version: {latestVersion}</Text>
          )}
        </Space>
      }
      open={open}
      onCancel={handleClose}
      width={900}
      footer={null}
      destroyOnClose
    >
      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px 0' }}>
          <Spin size="large" />
        </div>
      ) : (
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
          initialValues={{
            summary: '',
            market: '',
            product: '',
            traction: '',
            risks: '',
            open_questions: '',
          }}
        >
          <Paragraph type="secondary" style={{ marginBottom: 24 }}>
            Fill in each section below. Every time you save, a new version will be created,
            preserving the complete history of changes.
          </Paragraph>

          {sectionKeys.map((key, index) => (
            <div key={key}>
              {index > 0 && <Divider style={{ margin: '24px 0' }} />}
              <Form.Item
                label={
                  <Space direction="vertical" size={0}>
                    <Text strong style={{ fontSize: 16 }}>
                      {MEMO_SECTION_LABELS[key]}
                    </Text>
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      {MEMO_SECTION_DESCRIPTIONS[key]}
                    </Text>
                  </Space>
                }
                name={key}
              >
                <TextArea
                  rows={6}
                  placeholder={`Enter ${MEMO_SECTION_LABELS[key].toLowerCase()} details here... (Markdown supported)`}
                  style={{ fontFamily: 'monospace' }}
                />
              </Form.Item>
            </div>
          ))}

          <Divider />

          <Form.Item style={{ marginBottom: 0, marginTop: 32 }}>
            <Space style={{ width: '100%', justifyContent: 'space-between' }}>
              <Button
                icon={<HistoryOutlined />}
                onClick={onViewHistory}
                size="large"
              >
                View Version History
              </Button>
              <Space>
                <Button onClick={handleClose} size="large">
                  Cancel
                </Button>
                <Button
                  type="primary"
                  htmlType="submit"
                  icon={<SaveOutlined />}
                  loading={saving}
                  size="large"
                  style={{ background: '#667eea' }}
                >
                  Save New Version
                </Button>
              </Space>
            </Space>
          </Form.Item>
        </Form>
      )}
    </Modal>
  );
};

export default ICMemoEditor;


