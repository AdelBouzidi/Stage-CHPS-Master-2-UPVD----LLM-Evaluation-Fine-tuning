program decode_shift_demo
  implicit none
  character(len=*), parameter :: input_str = 'fgh'
  character(len=:), allocatable :: decoded
  integer :: i

  ! Call the decode_shift function
  decoded = decode_shift(input_str)

  ! Output the result
  print *, 'Decoded string:', decoded

contains

  function decode_shift(s) result(res)
    implicit none
    character(len=*), intent(in) :: s
    character(len=:), allocatable :: res
    integer :: i, len_s
    character(len=1) :: c

    len_s = len(s)
    allocate(character(len=len_s) :: res)

    do i = 1, len_s
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        if (c >= 'f') then
          res(i:i) = c - 5
        else
          res(i:i) = c + 21
        end if
      else if (c >= 'A' .and. c <= 'Z') then
        if (c >= 'F') then
          res(i:i) = c - 5
        else
          res(i:i) = c + 21
        end if
      else
        res(i:i) = c
      end if
    end do
  end function decode_shift

end program decode_shift_demo