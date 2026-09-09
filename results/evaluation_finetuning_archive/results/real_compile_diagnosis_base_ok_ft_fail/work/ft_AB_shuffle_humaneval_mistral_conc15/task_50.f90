program decode_shift_demo
  implicit none
  character(len=*), parameter :: input = 'fgh'
  character(len=:), allocatable :: result

  result = decode_shift(input)
  print *, 'Decoded:', result

contains

  function encode_shift(s) result(res)
    implicit none
    character(len=*), intent(in) :: s
    character(len=len(s)) :: res
    integer :: i, n
    character(len=1) :: c
    
    n = len(s)
    do i = 1, n
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        res(i:i) = achar(ichar(c) - 5)
      else if (c >= 'A' .and. c <= 'Z') then
        res(i:i) = achar(ichar(c) - 5)
      else
        res(i:i) = c
      end if
    end do
  end function encode_shift

  function decode_shift(s) result(res)
    implicit none
    character(len=*), intent(in) :: s
    character(len=len(s)) :: res
    integer :: i, n
    character(len=1) :: c
    
    n = len(s)
    do i = 1, n
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        res(i:i) = achar(ichar(c) + 5)
      else if (c >= 'A' .and. c <= 'Z') then
        res(i:i) = achar(ichar(c) + 5)
      else
        res(i:i) = c
      end if
    end do
  end function decode_shift

end program decode_shift_demo