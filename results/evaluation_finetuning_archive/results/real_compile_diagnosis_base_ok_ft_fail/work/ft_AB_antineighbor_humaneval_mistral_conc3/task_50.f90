program decode_shift_demo
  implicit none
  character(len=:), allocatable :: input, result
  integer :: i, len

  ! Read input from stdin
  read *, input

  ! Call the decode_shift function
  result = decode_shift(input)
  
  ! Output the result
  print *, result

contains

  function decode_shift(s) result(res)
    implicit none
    character(len=*), intent(in) :: s
    character(len=:), allocatable :: res
    integer :: i, len
    character(len=1) :: c
    
    len = len_trim(s)
    allocate(character(len=len) :: res)
    
    do i = 1, len
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        res(i:i) = char(ichar(c) - 5)
      else if (c >= 'A' .and. c <= 'Z') then
        res(i:i) = char(ichar(c) - 5)
      else
        res(i:i) = c
      end if
    end do
    
  end function decode_shift

end program decode_shift_demo