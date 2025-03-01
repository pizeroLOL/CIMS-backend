import React from 'react';
import { NavLink } from 'react-router-dom'; // 正确导入
import { Text,  Image } from '@fluentui/react-components'; // 直接导入 Stack
import {
  HomeFilled,
  HomeRegular,
  DeviceEqFilled,
  DeviceEqRegular,
  DocumentSettingsFilled,
  DocumentSettingsRegular,
  SettingsFilled,
  SettingsRegular
} from "@fluentui/react-icons";

function Sidebar() {
    return (
        <div className="sidebar">
            <div style={{paddingTop:10}}>
                {/* Logo 和文字 */}
                <div style={{display: 'flex', alignItems: 'center' }}>
                    <Image src="./logo.png" alt="Logo" width={50} height={50} />
                    <Text>
                        ClassIsland <br /> 集控控制台
                    </Text>
                </div>
                {/* 导航链接 */}
                <ul style={{ listStyleType: 'none', padding: 0 }}>
                    <li>
                        <NavLink to="/"
                         style={({ isActive }) => ({
                            display: 'block',
                            color: isActive ? 'blue' : 'black',
                            padding: '10px 15px',
                            textDecoration: 'none',
                        })}
                        >
                            {({ isActive } : {isActive:boolean}) => (  // 显式类型注解
                                <div style={{display:"flex", alignItems: 'center' }}>
                                    {isActive ? <HomeFilled /> : <HomeRegular />}
                                    <Text style={{paddingLeft:8}}>概览</Text>  {/* 使用 style, 而不是 styles */}
                                </div>
                            )}
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/device"
                         style={({ isActive }) => ({
                            display: 'block',
                            color: isActive ? 'blue' : 'black',
                            padding: '10px 15px',
                            textDecoration: 'none',
                        })}
                        >
                            {({ isActive } : {isActive:boolean}) => (
                                 <div style={{display:"flex", alignItems: 'center' }}>
                                    {isActive ? <DeviceEqFilled /> : <DeviceEqRegular />}
                                    <Text style={{paddingLeft:8}}>设备管理</Text>
                                </div>
                            )}
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/config"
                         style={({ isActive }) => ({
                            display: 'block',
                            color: isActive ? 'blue' : 'black',
                            padding: '10px 15px',
                            textDecoration: 'none',
                        })}
                        >
                        {({ isActive } : {isActive:boolean}) => (
                                <div style={{display:"flex", alignItems: 'center' }}>
                                {isActive ? <DocumentSettingsFilled /> : <DocumentSettingsRegular />}
                                <Text style={{paddingLeft:8}}>配置管理</Text>
                            </div>
                        )}
                        </NavLink>
                    </li>
                    <li>
                    <NavLink to="/settings"
                         style={({ isActive }) => ({
                            display: 'block',
                            color: isActive ? 'blue' : 'black',
                            padding: '10px 15px',
                            textDecoration: 'none',
                        })}
                        >
                        {({ isActive } : {isActive:boolean}) => (
                            <div style={{display:"flex", alignItems: 'center' }}>
                                {isActive ? <SettingsFilled /> : <SettingsRegular />}
                                <Text style={{paddingLeft:8}}>设置</Text>
                            </div>
                        )}
                        </NavLink>
                    </li>
                </ul>
                {/* 版本信息 */}
                <div style={{ padding: '10px 15px', fontSize: '12px' }}>
                    <p>服务器后端版本: v1.0.0 (示例)</p>
                    <p>WebUI 版本: v1.0.0 (示例)</p>
                </div>
            </div>
        </div>
    );
}

export default Sidebar;