import React, { useState, useEffect, useRef } from 'react';
import { TextField, Button, Box } from '@mui/material';
import { styled } from '@mui/material/styles';

interface ConfigEditorProps {
  value: string;
  onChange: (newValue: string) => void;
  onSave: (content: string) => Promise<void>;
  isEditing: boolean;
  setIsEditing: React.Dispatch<React.SetStateAction<boolean>>;
}

const StyledTextField = styled(TextField)({
  '& .MuiOutlinedInput-root': {
    '& textarea': {
      fontFamily: 'monospace', // 使用等宽字体
    },
  },
});

const ConfigEditor: React.FC<ConfigEditorProps> = ({ value, onChange, onSave, isEditing, setIsEditing }) => {
  const [localValue, setLocalValue] = useState(value);
  const editorRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  const handleLocalChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setLocalValue(event.target.value);
  };

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleSaveClick = async () => {
    try {
      await onSave(localValue);
      setIsEditing(false);
    } catch (error) {
      // 错误处理已经在父组件中通过 Snackbar 完成
    }
  };

  const handleCancelEdit = () => {
    setLocalValue(value); // 恢复到原始值
    setIsEditing(false);
  };


  return (
    <Box>
      <StyledTextField
        fullWidth
        multiline
        rows={20}
        variant="outlined"
        value={localValue}
        onChange={handleLocalChange}
        inputRef={editorRef}
        InputProps={{
          readOnly: !isEditing,
        }}
      />
      <Box mt={2} textAlign="right">
        {!isEditing ? (
          <Button variant="contained" color="primary" onClick={handleEditClick}>
            编辑
          </Button>
        ) : (
          <>
            <Button variant="contained" color="primary" onClick={handleSaveClick} sx={{ mr: 1 }}>
              保存
            </Button>
            <Button variant="outlined" onClick={handleCancelEdit}>
              取消
            </Button>
          </>
        )}
      </Box>
    </Box>
  );
};

export default ConfigEditor;