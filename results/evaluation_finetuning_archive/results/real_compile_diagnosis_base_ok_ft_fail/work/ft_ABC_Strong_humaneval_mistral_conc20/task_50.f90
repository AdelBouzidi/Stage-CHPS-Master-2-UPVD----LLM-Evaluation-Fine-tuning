program decode_shift_demo
  implicit none
  character(len=:), allocatable :: input_str, result
  
  read *, input_str
  call decode_shift(input_str, result)
  print *, result
contains

  subroutine decode_shift(s, result)
    character(len=*), intent(in) :: s
    character(len=:), allocatable, intent(out) :: result
    integer :: i, n
    character(len=1) :: c
    
    n = len_trim(s)
    allocate(character(len=n) :: result)
    
    do i = 1, n
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        result(i:i) = char(ichar(c) - 5)
      else if (c >= 'A' .and. c <= 'Z') then
        result(i:i) = char(ichar(c) - 5)
      else
        result(i:i) = c
      end if
    end do
  end subroutine decode_shift

end program decode_shift_demo