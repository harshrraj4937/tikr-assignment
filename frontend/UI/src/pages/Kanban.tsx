import React, { useState, useEffect } from 'react';
import { Card, Tag, Button, Space, Typography, Avatar, Badge, Spin, message, Modal, Form, Input, InputNumber } from 'antd';
import { ArrowLeftOutlined, PlusOutlined, DollarOutlined, LoadingOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { dealsAPI } from '../services/api';
import type { Deal, DealCreate } from '../types/deals';

const { Title, Text } = Typography;

const stages = ['Sourced', 'Screen', 'Diligence', 'IC', 'Invested', 'Passed'];

const stageColors: { [key: string]: string } = {
  'Sourced': '#8b5cf6',
  'Screen': '#3b82f6',
  'Diligence': '#f59e0b',
  'IC': '#ef4444',
  'Invested': '#10b981',
  'Passed': '#6b7280',
};

// Helper function to format check size
const formatCheckSize = (checkSize: string | null): string => {
  if (!checkSize) return 'N/A';
  const num = parseFloat(checkSize);
  if (isNaN(num)) return checkSize;
  
  if (num >= 1000000) {
    return `$${(num / 1000000).toFixed(1)}M`;
  } else if (num >= 1000) {
    return `$${(num / 1000).toFixed(0)}K`;
  }
  return `$${num.toFixed(0)}`;
};

const Kanban: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [deals, setDeals] = useState<Deal[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [draggedDeal, setDraggedDeal] = useState<Deal | null>(null);
  const [draggedOverStage, setDraggedOverStage] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [isCreating, setIsCreating] = useState<boolean>(false);
  const [form] = Form.useForm();

  // Fetch deals on component mount
  useEffect(() => {
    fetchDeals();
  }, []);

  const fetchDeals = async () => {
    try {
      setLoading(true);
      const fetchedDeals = await dealsAPI.listDeals();
      setDeals(fetchedDeals);
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Failed to load deals');
      console.error('Error fetching deals:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBackToDashboard = () => {
    navigate('/dashboard');
  };

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    form.resetFields();
  };

  const handleCreateDeal = async (values: DealCreate) => {
    try {
      setIsCreating(true);
      const newDeal = await dealsAPI.createDeal(values);
      setDeals([newDeal, ...deals]);
      message.success(`Deal "${newDeal.name}" created successfully!`);
      handleCloseModal();
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Failed to create deal');
      console.error('Error creating deal:', error);
    } finally {
      setIsCreating(false);
    }
  };

  const handleDragStart = (e: React.DragEvent, deal: Deal) => {
    setDraggedDeal(deal);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragEnd = () => {
    setDraggedDeal(null);
    setDraggedOverStage(null);
  };

  const handleDragOver = (e: React.DragEvent, stage: string) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    setDraggedOverStage(stage);
  };

  const handleDragLeave = () => {
    setDraggedOverStage(null);
  };

  const handleDrop = async (e: React.DragEvent, targetStage: string) => {
    e.preventDefault();
    if (draggedDeal && draggedDeal.stage !== targetStage) {
      const oldStage = draggedDeal.stage;
      
      // Optimistically update UI
      const updatedDeals = deals.map(deal =>
        deal.id === draggedDeal.id
          ? { ...deal, stage: targetStage, updated_at: new Date().toISOString() }
          : deal
      );
      setDeals(updatedDeals);
      
      try {
        // Call API to update the stage
        await dealsAPI.updateDealStage(draggedDeal.id, targetStage);
        message.success(`Moved ${draggedDeal.name} from ${oldStage} to ${targetStage}`);
      } catch (error: any) {
        // Revert on error
        setDeals(deals);
        message.error(error.response?.data?.detail || 'Failed to update deal stage');
        console.error('Error updating deal stage:', error);
      }
    }
    setDraggedOverStage(null);
  };

  const getDealsByStage = (stage: string) => {
    return deals.filter(deal => deal.stage === stage);
  };

  const DealCard: React.FC<{ deal: Deal }> = ({ deal }) => {
    const ownerName = deal.owner.first_name && deal.owner.last_name
      ? `${deal.owner.first_name} ${deal.owner.last_name}`
      : deal.owner.username;
    const ownerInitial = deal.owner.first_name?.charAt(0) || deal.owner.username.charAt(0);
    
    return (
      <Card
        draggable
        onDragStart={(e) => handleDragStart(e, deal)}
        onDragEnd={handleDragEnd}
        style={{
          marginBottom: 12,
          cursor: 'grab',
          border: draggedDeal?.id === deal.id ? '2px dashed #667eea' : '1px solid #e8e8e8',
          opacity: draggedDeal?.id === deal.id ? 0.5 : 1,
          transition: 'all 0.2s ease',
        }}
        bodyStyle={{ padding: 16 }}
        hoverable
      >
        <Space direction="vertical" size="small" style={{ width: '100%' }}>
          <Text strong style={{ fontSize: 16 }}>{deal.name}</Text>
          
          {deal.company_url && (
            <a 
              href={deal.company_url} 
              target="_blank" 
              rel="noopener noreferrer"
              style={{ fontSize: 12, color: '#667eea' }}
              onClick={(e) => e.stopPropagation()}
            >
              {deal.company_url}
            </a>
          )}
          
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 8 }}>
            {deal.round && <Tag color="blue">{deal.round}</Tag>}
            {deal.check_size && (
              <Space size={4}>
                <DollarOutlined style={{ color: '#10b981' }} />
                <Text strong style={{ color: '#10b981' }}>{formatCheckSize(deal.check_size)}</Text>
              </Space>
            )}
          </div>
          
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginTop: 8,
            paddingTop: 8,
            borderTop: '1px solid #f0f0f0'
          }}>
            <Space size={4}>
              <Avatar size="small" style={{ backgroundColor: '#667eea' }}>
                {ownerInitial}
              </Avatar>
              <Text type="secondary" style={{ fontSize: 12 }}>{ownerName}</Text>
            </Space>
          </div>
        </Space>
      </Card>
    );
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px'
    }}>
      <div style={{ maxWidth: 1600, margin: '0 auto' }}>
        {/* Header */}
        <div style={{
          background: 'white',
          padding: '20px 30px',
          borderRadius: '12px',
          marginBottom: 20,
          boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <Space size="large">
            <Button
              icon={<ArrowLeftOutlined />}
              onClick={handleBackToDashboard}
              size="large"
            >
              Back to Dashboard
            </Button>
            <div>
              <Title level={2} style={{ margin: 0 }}>
                Deal Pipeline
              </Title>
              <Text type="secondary">
                Drag and drop deals to move them through stages
              </Text>
            </div>
          </Space>
          
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleOpenModal}
            size="large"
            style={{ background: '#667eea' }}
          >
            Add New Deal
          </Button>
        </div>

        {/* Kanban Board */}
        {loading ? (
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '60vh',
            background: 'white',
            borderRadius: '12px',
          }}>
            <Spin 
              indicator={<LoadingOutlined style={{ fontSize: 48, color: '#667eea' }} spin />}
              tip="Loading deals..."
            />
          </div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: `repeat(${stages.length}, 1fr)`,
            gap: 16,
            overflowX: 'auto',
          }}>
            {stages.map(stage => {
            const stageDeals = getDealsByStage(stage);
            const isDropTarget = draggedOverStage === stage && draggedDeal?.stage !== stage;
            
            return (
              <div
                key={stage}
                onDragOver={(e) => handleDragOver(e, stage)}
                onDragLeave={handleDragLeave}
                onDrop={(e) => handleDrop(e, stage)}
                style={{
                  minWidth: 280,
                  transition: 'all 0.2s ease',
                }}
              >
                <Card
                  style={{
                    background: isDropTarget ? '#f0f9ff' : 'white',
                    border: isDropTarget ? '2px dashed #667eea' : '1px solid #e8e8e8',
                    borderRadius: '12px',
                    height: '100%',
                    minHeight: 'calc(100vh - 200px)',
                    boxShadow: isDropTarget 
                      ? '0 8px 30px rgba(102, 126, 234, 0.3)' 
                      : '0 4px 20px rgba(0,0,0,0.1)',
                    transition: 'all 0.3s ease',
                  }}
                  bodyStyle={{ padding: 16 }}
                >
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center',
                    marginBottom: 16,
                    paddingBottom: 12,
                    borderBottom: `3px solid ${stageColors[stage]}`
                  }}>
                    <Space>
                      <div
                        style={{
                          width: 12,
                          height: 12,
                          borderRadius: '50%',
                          backgroundColor: stageColors[stage],
                        }}
                      />
                      <Text strong style={{ fontSize: 16 }}>
                        {stage}
                      </Text>
                    </Space>
                    <Badge 
                      count={stageDeals.length} 
                      style={{ backgroundColor: stageColors[stage] }}
                    />
                  </div>
                  
                  <div>
                    {stageDeals.map(deal => (
                      <DealCard key={deal.id} deal={deal} />
                    ))}
                    
                    {stageDeals.length === 0 && (
                      <div style={{
                        textAlign: 'center',
                        padding: '40px 20px',
                        color: '#999',
                      }}>
                        <Text type="secondary">No deals in this stage</Text>
                      </div>
                    )}
                  </div>
                </Card>
              </div>
            );
          })}
          </div>
        )}

        {/* Create Deal Modal */}
        <Modal
          title="Create New Deal"
          open={isModalOpen}
          onCancel={handleCloseModal}
          footer={null}
          width={600}
        >
          <Form
            form={form}
            layout="vertical"
            onFinish={handleCreateDeal}
            style={{ marginTop: 24 }}
          >
            <Form.Item
              label="Deal Name"
              name="name"
              rules={[{ required: true, message: 'Please enter the deal name' }]}
            >
              <Input placeholder="e.g., TechStart AI" size="large" />
            </Form.Item>

            <Form.Item
              label="Company URL"
              name="company_url"
            >
              <Input placeholder="https://example.com" size="large" />
            </Form.Item>

            <Form.Item
              label="Round"
              name="round"
            >
              <Input placeholder="e.g., Seed, Series A" size="large" />
            </Form.Item>

            <Form.Item
              label="Check Size"
              name="check_size"
              help="Enter amount in dollars (e.g., 500000 for $500K)"
            >
              <InputNumber
                placeholder="500000"
                size="large"
                style={{ width: '100%' }}
                min={0}
                formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                parser={value => value!.replace(/\$\s?|(,*)/g, '')}
              />
            </Form.Item>

            <Form.Item style={{ marginBottom: 0, marginTop: 32 }}>
              <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
                <Button onClick={handleCloseModal} size="large">
                  Cancel
                </Button>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={isCreating}
                  size="large"
                  style={{ background: '#667eea' }}
                >
                  Create Deal
                </Button>
              </Space>
            </Form.Item>
          </Form>
        </Modal>
      </div>
    </div>
  );
};

export default Kanban;

