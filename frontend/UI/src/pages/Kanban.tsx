import React, { useState } from 'react';
import { Card, Tag, Button, Space, Typography, Avatar, Badge } from 'antd';
import { ArrowLeftOutlined, PlusOutlined, DollarOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const { Title, Text } = Typography;

interface Deal {
  id: string;
  name: string;
  company_url: string;
  owner: string;
  stage: string;
  round: string;
  check_size: string;
  status: string;
  created_at: string;
  updated_at: string;
}

const stages = ['Sourced', 'Screen', 'Diligence', 'IC', 'Invested', 'Passed'];

const stageColors: { [key: string]: string } = {
  'Sourced': '#8b5cf6',
  'Screen': '#3b82f6',
  'Diligence': '#f59e0b',
  'IC': '#ef4444',
  'Invested': '#10b981',
  'Passed': '#6b7280',
};

// Sample data for demonstration
const sampleDeals: Deal[] = [
  {
    id: '1',
    name: 'TechStart AI',
    company_url: 'https://techstart.ai',
    owner: 'John Doe',
    stage: 'Sourced',
    round: 'Seed',
    check_size: '$500K',
    status: 'active',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: '2',
    name: 'FinanceFlow',
    company_url: 'https://financeflow.com',
    owner: 'Jane Smith',
    stage: 'Screen',
    round: 'Series A',
    check_size: '$2M',
    status: 'active',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: '3',
    name: 'HealthTech Pro',
    company_url: 'https://healthtech.pro',
    owner: 'Mike Johnson',
    stage: 'Diligence',
    round: 'Seed',
    check_size: '$750K',
    status: 'active',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: '4',
    name: 'CloudNine',
    company_url: 'https://cloudnine.io',
    owner: 'Sarah Williams',
    stage: 'IC',
    round: 'Series B',
    check_size: '$5M',
    status: 'active',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: '5',
    name: 'DataInsights',
    company_url: 'https://datainsights.com',
    owner: 'John Doe',
    stage: 'Invested',
    round: 'Series A',
    check_size: '$3M',
    status: 'invested',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

const Kanban: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [deals, setDeals] = useState<Deal[]>(sampleDeals);
  const [draggedDeal, setDraggedDeal] = useState<Deal | null>(null);
  const [draggedOverStage, setDraggedOverStage] = useState<string | null>(null);

  const handleBackToDashboard = () => {
    navigate('/dashboard');
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

  const handleDrop = (e: React.DragEvent, targetStage: string) => {
    e.preventDefault();
    if (draggedDeal && draggedDeal.stage !== targetStage) {
      const updatedDeals = deals.map(deal =>
        deal.id === draggedDeal.id
          ? { ...deal, stage: targetStage, updated_at: new Date().toISOString() }
          : deal
      );
      setDeals(updatedDeals);
      
      // Here you would typically make an API call to update the backend
      console.log(`Moved ${draggedDeal.name} from ${draggedDeal.stage} to ${targetStage}`);
    }
    setDraggedOverStage(null);
  };

  const getDealsByStage = (stage: string) => {
    return deals.filter(deal => deal.stage === stage);
  };

  const DealCard: React.FC<{ deal: Deal }> = ({ deal }) => (
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
        
        <a 
          href={deal.company_url} 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ fontSize: 12, color: '#667eea' }}
          onClick={(e) => e.stopPropagation()}
        >
          {deal.company_url}
        </a>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 8 }}>
          <Tag color="blue">{deal.round}</Tag>
          <Space size={4}>
            <DollarOutlined style={{ color: '#10b981' }} />
            <Text strong style={{ color: '#10b981' }}>{deal.check_size}</Text>
          </Space>
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
              {deal.owner.charAt(0)}
            </Avatar>
            <Text type="secondary" style={{ fontSize: 12 }}>{deal.owner}</Text>
          </Space>
        </div>
      </Space>
    </Card>
  );

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
            size="large"
            style={{ background: '#667eea' }}
          >
            Add New Deal
          </Button>
        </div>

        {/* Kanban Board */}
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
      </div>
    </div>
  );
};

export default Kanban;

